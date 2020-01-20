from typing import List

from aiohttp import web
from sqlalchemy import and_, delete, insert, select, update

from athenian.api import FriendlyJson
from athenian.api.controllers.reposet import fetch_reposet
from athenian.api.controllers.response import response, ResponseError
from athenian.api.models.state.models import RepositorySet, UserAccount
from athenian.api.models.web import CreatedIdentifier, ForbiddenError
from athenian.api.models.web.repository_set_create_request import RepositorySetCreateRequest
from athenian.api.models.web.repository_set_list_item import RepositorySetListItem
from athenian.api.request import AthenianWebRequest


async def create_reposet(request: AthenianWebRequest, body: dict) -> web.Response:
    """Create a repository set.

    :param body: List of repositories to group.
    """
    body = RepositorySetCreateRequest.from_dict(body)
    user = request.user.id
    account = body.account
    status = await request.sdb.fetch_one(select([UserAccount.is_admin]).where(
        and_(UserAccount.user_id == user, UserAccount.account_id == account)))
    if status is None:
        return ResponseError(ForbiddenError(
            detail="User %s is not in the account %d" % (user, account))).response
    if not status[UserAccount.is_admin.key]:
        return ResponseError(ForbiddenError(
            detail="User %s is not an admin of the account %d" % (user, account))).response
    # TODO(vmarkovtsev): get user's repos and check the access
    rs = RepositorySet(owner=account, items=body.items)
    rs.create_defaults()
    rid = await request.sdb.execute(insert(RepositorySet).values(rs.explode()))
    return response(CreatedIdentifier(rid))


async def delete_reposet(request: AthenianWebRequest, id: int) -> web.Response:
    """Delete a repository set.

    :param id: Numeric identifier of the repository set to delete.
    :type id: int
    """
    try:
        _, is_admin = await fetch_reposet(id, [], request.sdb, request.user, None)
    except ResponseError as e:
        return e.response
    if not is_admin:
        return ResponseError(ForbiddenError(
            detail="User %s may not modify reposet %d" % (request.user.id, id))).response
    await request.sdb.execute(delete(RepositorySet).where(RepositorySet.id == id))
    return web.Response(status=200)


async def get_reposet(request: AthenianWebRequest, id: int) -> web.Response:
    """List a repository set.

    :param id: Numeric identifier of the repository set to list.
    :type id: int
    """
    try:
        rs, _ = await fetch_reposet(id, [RepositorySet.items], request.sdb, request.user, None)
    except ResponseError as e:
        return e.response
    # "items" collides with dict.items() so we have to access the list via []
    return web.json_response(rs.items, status=200)


async def update_reposet(request: AthenianWebRequest, id: int, body: List[str]) -> web.Response:
    """Update a repository set.

    :param id: Numeric identifier of the repository set to update.
    :type id: int
    :param body: New list of repositories in the group.
    """
    try:
        rs, is_admin = await fetch_reposet(id, [RepositorySet], request.sdb, request.user, None)
    except ResponseError as e:
        return e.response
    if not is_admin:
        return ResponseError(ForbiddenError(
            detail="User %s may not modify reposet %d" % (request.user.id, id))).response
    rs.items = body
    rs.refresh()
    # TODO(vmarkovtsev): get user's repos and check the access
    await request.sdb.execute(update(RepositorySet)
                              .where(RepositorySet.id == id)
                              .values(rs.explode()))
    return web.json_response(body, status=200)


async def list_reposets(request: AthenianWebRequest, id: int) -> web.Response:
    """List the current user's repository sets."""
    status = await request.sdb.fetch_one(select([UserAccount.is_admin]).where(
        and_(UserAccount.user_id == request.user.id, UserAccount.account_id == id)))
    if status is None:
        return ResponseError(ForbiddenError(
            detail="User %s is not in the account %d" % (request.user.id, id))).response
    rss = await request.sdb.fetch_all(
        select([RepositorySet]).where(RepositorySet.owner == id))
    items = [RepositorySetListItem(
        id=rs[RepositorySet.id.key],
        created=rs[RepositorySet.created_at.key],
        updated=rs[RepositorySet.updated_at.key],
        items_count=rs[RepositorySet.items_count.key],
    ).to_dict() for rs in rss]
    return web.json_response(items, status=200, dumps=FriendlyJson.dumps)
