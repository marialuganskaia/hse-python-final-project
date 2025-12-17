from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from ..use_cases.start_user import StartUserUseCase
from ..use_cases.select_hackathon import SelectHackathonByCodeUseCase
from ..use_cases.get_schedule import GetScheduleUseCase
from ..use_cases.get_rules import GetRulesUseCase
from ..use_cases.get_faq import GetFAQUseCase
from ..use_cases.notifications import SubscribeNotificationsUseCase, UnsubscribeNotificationsUseCase
from ..use_cases.list_hackathons import ListHackathonsUseCase
from ..use_cases.get_hackathon_info import GetHackathonInfoUseCase
from ..use_cases.get_upcoming_events import GetUpcomingEventsUseCase
from ..use_cases.get_admin_stats import GetAdminStatsUseCase
from ..use_cases.send_broadcast import SendBroadcastUseCase
from ..use_cases.finish_hackathon import FinishHackathonUseCase

from .repositories import RepositoryProvider


@dataclass(frozen=True)
class UseCaseProvider:
    """Container with ready-to-use participant use cases."""
    
    start_user: StartUserUseCase
    select_hackathon_by_code: SelectHackathonByCodeUseCase
    get_schedule: GetScheduleUseCase
    get_rules: GetRulesUseCase
    get_faq: GetFAQUseCase
    subscribe_notifications: SubscribeNotificationsUseCase
    unsubscribe_notifications: UnsubscribeNotificationsUseCase
    list_hackathons: ListHackathonsUseCase
    get_hackathon_info: GetHackathonInfoUseCase
    get_upcoming_events: GetUpcomingEventsUseCase
    get_admin_stats: GetAdminStatsUseCase
    send_broadcast: SendBroadcastUseCase
    finish_hackathon: FinishHackathonUseCase


def build_use_case_provider(session: AsyncSession) -> UseCaseProvider:
    repos = RepositoryProvider(session=session)

    return UseCaseProvider(
        start_user=StartUserUseCase(user_repo=repos.user_repo()),
        select_hackathon_by_code=SelectHackathonByCodeUseCase(
            user_repo=repos.user_repo(),
            hackathon_repo=repos.hackathon_repo(),
        ),
        get_schedule=GetScheduleUseCase(
            user_repo=repos.user_repo(),
            event_repo=repos.event_repo(),
        ),
        get_rules=GetRulesUseCase(
            user_repo=repos.user_repo(),
            rules_repo=repos.rules_repo(),
        ),
        get_faq=GetFAQUseCase(
            user_repo=repos.user_repo(),
            faq_repo=repos.faq_repo(),
        ),
        subscribe_notifications=SubscribeNotificationsUseCase(
            user_repo=repos.user_repo(),
            subscription_repo=repos.subscription_repo(),
        ),
        unsubscribe_notifications=UnsubscribeNotificationsUseCase(
            user_repo=repos.user_repo(),
            subscription_repo=repos.subscription_repo(),
        ),
        list_hackathons=ListHackathonsUseCase(
            hackathon_repo=repos.hackathon_repo(),
        ),
        get_hackathon_info=GetHackathonInfoUseCase(
            user_repo=repos.user_repo(),
            hackathon_repo=repos.hackathon_repo(),
            subscription_repo=repos.subscription_repo(),
        ),
        get_upcoming_events=GetUpcomingEventsUseCase(
            event_repo=repos.event_repo()
        ),
        get_admin_stats=GetAdminStatsUseCase(
            user_repo=repos.user_repo(),
            subscription_repo=repos.subscription_repo(),
            hackathon_repo=repos.hackathon_repo(),
        ),
        send_broadcast=SendBroadcastUseCase(
            user_repo=repos.user_repo(),
            subscription_repo=repos.subscription_repo(),
        ),
        finish_hackathon=FinishHackathonUseCase(
            hackathon_repo=repos.hackathon_repo(),
            subscription_repo=repos.subscription_repo(),
        ),
    )
