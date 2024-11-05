from enum import Enum
import requests
from typing import Optional, Union, List

from .baseendpoint import BaseEndpoint
from .. import resources
from ..filters import market_filter, time_range
from ..utils import clean_locals


class MarketProjection(str, Enum):
    COMPETITION = "COMPETITION"
    """
    If not selected then the competition will not be returned with marketCatalogue
    """

    EVENT = "EVENT"
    """
    If not selected then the event will not be returned with marketCatalogue
    """

    EVENT_TYPE = "EVENT_TYPE"
    """
    If not selected then the eventType will not be returned with marketCatalogue
    """

    MARKET_START_TIME = "MARKET_START_TIME"
    """
    If not selected then the start time will not be returned with marketCatalogue
    """

    MARKET_DESCRIPTION = "MARKET_DESCRIPTION"
    """
    If not selected then the description will not be returned with marketCatalogue
    """

    RUNNER_DESCRIPTION = "RUNNER_DESCRIPTION"
    """
    If not selected then the runners will not be returned with marketCatalogue
    """

    RUNNER_METADATA = "RUNNER_METADATA"
    """
    If not selected then the runner metadata will not be returned with marketCatalogue. If selected then RUNNER_DESCRIPTION will also be returned regardless of whether it is included as a market projection.
    """


class PriceData(str, Enum):

    SP_AVAILABLE = "SP_AVAILABLE"
    """
    Amount available for the BSP auction.
    """

    SP_TRADED = "SP_TRADED"
    """
    Amount traded in the BSP auction.
    """

    EX_BEST_OFFERS = "EX_BEST_OFFERS"
    """
    Only the best prices available for each runner, to requested price depth.
    """

    EX_ALL_OFFERS = "EX_ALL_OFFERS"
    """
    EX_ALL_OFFERS trumps EX_BEST_OFFERS if both settings are present
    """

    EX_TRADED = "EX_TRADED"
    """
    Amount traded on the exchange.
    """


class MatchProjection(str, Enum):

    NO_ROLLUP = "NO_ROLLUP"
    """
    No rollup, return raw fragments
    """

    ROLLED_UP_BY_PRICE = "ROLLED_UP_BY_PRICE"
    """
    Rollup matched amounts by distinct matched prices per side.
    """

    ROLLED_UP_BY_AVG_PRICE = "ROLLED_UP_BY_AVG_PRICE"
    """
    Rollup matched amounts by average matched price per side
    """


class OrderProjection(str, Enum):
    ALL = "ALL"
    """
    EXECUTABLE and EXECUTION_COMPLETE orders
    """

    EXECUTABLE = "EXECUTABLE"
    """
    An order that has a remaining unmatched portion. This is either a fully unmatched or partially matched bet (order)
    """

    EXECUTION_COMPLETE = "EXECUTION_COMPLETE"
    """
    An order that does not have any remaining unmatched portion.  This is a fully matched bet (order).
    """


class MarketStatus(str, Enum):

    INACTIVE = "INACTIVE"
    """
    The market has been created but isn't yet available.
    """

    OPEN = "OPEN"
    """
    The market is open for betting.
    """

    SUSPENDED = "SUSPENDED"
    """
    The market is suspended and not available for betting.
    """

    CLOSED = "CLOSED"
    """
    The market has been settled and is no longer available for betting.
    """


class RunnerStatus(str, Enum):

    ACTIVE = "ACTIVE"
    """
    ACTIVE
    """

    WINNER = "WINNER"
    """
    WINNER
    """

    LOSER = "LOSER"
    """
    LOSER
    """

    PLACED = "PLACED"
    """
    The runner was placed, applies to EACH_WAY marketTypes only.
    """

    REMOVED_VACANT = "REMOVED_VACANT"
    """
    REMOVED_VACANT applies to Greyhounds. Greyhound markets always return a fixed number of runners (traps). If a dog has been removed, the trap is shown as vacant.
    """

    REMOVED = "REMOVED"
    """
    REMOVED
    """

    HIDDEN = "HIDDEN"
    """
    The selection is hidden from the market.  This occurs in Horse Racing markets were runners is hidden when it is doesn’t hold an official entry following an entry stage. This could be because the horse was never entered or because they have been scratched from a race at a declaration stage. All matched customer bet prices are set to 1.0 even if there are later supplementary stages. Should it appear likely that a specific runner may actually be supplemented into the race this runner will be reinstated with all matched customer bets set back to the original prices.
    """


class TimeGranularity(str, Enum):

    DAYS = "DAYS"

    HOURS = "HOURS"

    MINUTES = "MINUTES"


class Side(str, Enum):

    BACK = "BACK"
    """
    To back a team, horse or outcome is to bet on the selection to win. For LINE markets a Back bet refers to a SELL line. A SELL line will win if the outcome is LESS THAN the taken line (price)  
    """

    LAY = "LAY"
    """
    To lay a team, horse, or outcome is to bet on the selection to lose. For LINE markets a Lay bet refers to a BUY line. A BUY line will win if the outcome is MORE THAN the taken line (price) 
    """


class OrderStatus(str, Enum):

    PENDING = "PENDING"
    """
    An asynchronous order is yet to be processed. Once the bet has been processed by the exchange
    (including waiting for any in-play delay), the result will be reported and available on the
    Exchange Stream API and API NG.
    Not a valid search criteria on MarketFilter
    """

    EXECUTION_COMPLETE = "EXECUTION_COMPLETE"
    """
    An order that does not have any remaining unmatched portion.
    """

    EXECUTABLE = "EXECUTABLE"
    """
    An order that has a remaining unmatched portion.
    """

    EXPIRED = "EXPIRED"
    """
    The order is no longer available for execution due to its time in force constraint.
    In the case of FILL_OR_KILL orders, this means the order has been killed because it could not be filled to your specifications.
    Not a valid search criteria on MarketFilter
    """


class OrderBy(str, Enum):

    BY_BET = "BY_BET"
    """
    @Deprecated Use BY_PLACE_TIME instead. Order by placed time, then bet id.
    """

    BY_MARKET = "BY_MARKET"
    """
    Order by market id, then placed time, then bet id.
    """

    BY_MATCH_TIME = "BY_MATCH_TIME"
    """
    Order by time of last matched fragment (if any), then placed time, then bet id. Filters out orders which have no matched date. The dateRange filter (if specified) is applied to the matched date.
    """

    BY_PLACE_TIME = "BY_PLACE_TIME"
    """
    Order by placed time, then bet id. This is an alias of to be deprecated BY_BET. The dateRange filter (if specified) is applied to the placed date.
    """

    BY_SETTLED_TIME = "BY_SETTLED_TIME"
    """
    Order by time of last settled fragment (if any due to partial market settlement), then by last match time, then placed time, then bet id. Filters out orders which have not been settled. The dateRange filter (if specified) is applied to the settled date.
    """

    BY_VOID_TIME = "BY_VOID_TIME"
    """
    Order by time of last voided fragment (if any), then by last match time, then placed time, then bet id. Filters out orders which have not been voided. The dateRange filter (if specified) is applied to the voided date.
    """


class SortDir(str, Enum):

    EARLIEST_TO_LATEST = "EARLIEST_TO_LATEST"
    """
    Order from earliest value to latest e.g. lowest betId is first in the results.
    """

    LATEST_TO_EARLIEST = "LATEST_TO_EARLIEST"
    """
    Order from the latest value to the earliest e.g. highest betId is first in the results.
    """


class OrderType(str, Enum):

    LIMIT = "LIMIT"
    """
    A normal exchange limit order for immediate execution
    """

    LIMIT_ON_CLOSE = "LIMIT_ON_CLOSE"
    """
    Limit order for the auction (SP)
    """

    MARKET_ON_CLOSE = "MARKET_ON_CLOSE"
    """
    Market order for the auction (SP)
    """


class MarketSort(str, Enum):

    MINIMUM_TRADED = "MINIMUM_TRADED"
    """
    Minimum traded volume
    """

    MAXIMUM_TRADED = "MAXIMUM_TRADED"
    """
    Maximum traded volume
    """

    MINIMUM_AVAILABLE = "MINIMUM_AVAILABLE"
    """
    Minimum available to match
    """

    MAXIMUM_AVAILABLE = "MAXIMUM_AVAILABLE"
    """
    Maximum available to match
    """

    FIRST_TO_START = "FIRST_TO_START"
    """
    The closest markets based on their expected start time
    """

    LAST_TO_START = "LAST_TO_START"
    """
    The most distant markets based on their expected start time
    """


class MarketBettingType(str, Enum):

    ODDS = "ODDS"
    """
    Odds Market - Any market that doesn't fit any any of the below categories.
    """

    LINE = "LINE"
    """
    Line Market - LINE markets operate at even-money odds of 2.0. However, price for these markets refers to the line positions available as defined by the markets min-max range and interval steps. Customers either Buy a line (LAY bet, winning if outcome is greater than the taken line (price)) or Sell a line (BACK bet, winning if outcome is less than the taken line (price)). If settled outcome equals the taken line, stake is returned.
    """

    RANGE = "RANGE"
    """
    Range Market - Now Deprecated
    """

    ASIAN_HANDICAP_DOUBLE_LINE = "ASIAN_HANDICAP_DOUBLE_LINE"
    """
    Asian Handicap Market - A traditional Asian handicap market. Can be identified by marketType ASIAN_HANDICAP
    """

    ASIAN_HANDICAP_SINGLE_LINE = "ASIAN_HANDICAP_SINGLE_LINE"
    """
    Asian Single Line Market - A market in which there can be 0 or multiple winners. e,.g marketType TOTAL_GOALS
    """

    FIXED_ODDS = "FIXED_ODDS"
    """
    Sportsbook Odds Market. This type is deprecated and will be removed in future releases, when Sportsbook markets will be represented as ODDS market but with a different product type
    """


class ExecutionReportStatus(str, Enum):

    SUCCESS = "SUCCESS"
    """
    Order processed successfully
    """

    FAILURE = "FAILURE"
    """
    Order failed.
    """

    PROCESSED_WITH_ERRORS = "PROCESSED_WITH_ERRORS"
    """
    The order itself has been accepted, but at least one (possibly all) actions have generated errors. This error only occurs for replaceOrders, cancelOrders and updateOrders operations.
    In normal circumstances the /wiki/spaces/BFAPIBETA/pages/1212454 operation will not return PROCESSED_WITH_ERRORS status as it is an atomic operation.  PLEASE NOTE: if the 'Best Execution' features is switched off, placeOrders can return ‘PROCESSED_WITH_ERRORS’ meaning that some bets can be rejected and other placed when submitted in the same PlaceInstruction
    """

    TIMEOUT = "TIMEOUT"
    """
    The order timed out & the status of the bet is unknown.  If a TIMEOUT error occurs on a placeOrders/replaceOrders request, you should check listCurrentOrders to verify the status of your bets before placing further orders. Please Note: Timeouts will occur after 5 seconds of attempting to process the bet but please allow up to 15 seconds for a timed out order to appear. After this time any unprocessed bets will automatically be Lapsed and no longer be available on the Exchange.
    """


class ExecutionReportErrorCode(str, Enum):

    ERROR_IN_MATCHER = "ERROR_IN_MATCHER"
    """
    The matcher is not healthy. Please note: The error will also be returned is you attempt concurrent 'cancel all' bets requests using cancelOrders which isn't permitted.
    """
    PROCESSED_WITH_ERRORS = "PROCESSED_WITH_ERRORS"
    """
    The order itself has been accepted, but at least one (possibly all) actions have generated errors
    """
    BET_ACTION_ERROR = "BET_ACTION_ERROR"
    """
    There is an error with an action that has caused the entire order to be rejected. Check the instructionReports errorCode for the reason for the rejection of the order.
    """
    INVALID_ACCOUNT_STATE = "INVALID_ACCOUNT_STATE"
    """
    Order rejected due to the account's status (suspended, inactive, dup cards)
    """
    INVALID_WALLET_STATUS = "INVALID_WALLET_STATUS"
    """
    Order rejected due to the account's wallet's status
    """
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    """
    Account has exceeded its exposure limit or available to bet limit
    """
    LOSS_LIMIT_EXCEEDED = "LOSS_LIMIT_EXCEEDED"
    """
    The account has exceed the self imposed loss limit
    """
    MARKET_SUSPENDED = "MARKET_SUSPENDED"
    """
    Market is suspended
    """
    MARKET_NOT_OPEN_FOR_BETTING = "MARKET_NOT_OPEN_FOR_BETTING"
    """
    Market is not open for betting. It is either not yet active, suspended or closed awaiting settlement.
    """
    DUPLICATE_TRANSACTION = "DUPLICATE_TRANSACTION"
    """
    Duplicate customer reference data submitted - Please note: There is a time window associated with the de-duplication of duplicate submissions which is 60 second
    """
    INVALID_ORDER = "INVALID_ORDER"
    """
    Order cannot be accepted by the matcher due to the combination of actions. For example, bets being edited are not on the same market, or order includes both edits and placement
    """
    INVALID_MARKET_ID = "INVALID_MARKET_ID"
    """
    Market doesn't exist
    """
    PERMISSION_DENIED = "PERMISSION_DENIED"
    """
    Business rules do not allow order to be placed. You are either attempting to place the order using a Delayed Application Key or from a restricted jurisdiction (i.e. USA)
    """
    DUPLICATE_BETIDS = "DUPLICATE_BETIDS"
    """
    Duplicate bet ids found. For example, you've included the same betId more than once in a single cancelOrders request.
    """
    NO_ACTION_REQUIRED = "NO_ACTION_REQUIRED"
    """
    Order hasn't been passed to matcher as system detected there will be no state change
    """
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    """
    The requested service is unavailable
    """
    REJECTED_BY_REGULATOR = "REJECTED_BY_REGULATOR"
    """
    The regulator rejected the order. On the Italian Exchange this error will occur if more than 50 bets are sent in a single placeOrders request.
    """
    NO_CHASING = "NO_CHASING"
    """
    A specific error code that relates to Spanish Exchange markets only which indicates that the bet placed contravenes the Spanish regulatory rules relating to loss chasing.
    """
    REGULATOR_IS_NOT_AVAILABLE = "REGULATOR_IS_NOT_AVAILABLE"
    """
    The underlying regulator service is not available.
    """
    TOO_MANY_INSTRUCTIONS = "TOO_MANY_INSTRUCTIONS"
    """
    The amount of orders exceeded the maximum amount allowed to be executed
    """
    INVALID_MARKET_VERSION = "INVALID_MARKET_VERSION"
    """
    The supplied market version is invalid. Max length allowed for market version is 12.
    """
    INVALID_PROFIT_RATIO = "INVALID_PROFIT_RATIO"
    """
    The order falls outside the permitted price and size combination.
    """


class PersistenceType(str, Enum):
    LAPSE = "LAPSE"
    """
    Lapse (cancel) the order automatically when the market is turned in play if the bet is unmatched
    """

    PERSIST = "PERSIST"
    """
    Persist the unmatched order to in-play. The bet will be placed automatically into the in-play market at the start of the event.
    Once in play, the bet won't be cancelled by Betfair if a material event takes place and will be available until matched or cancelled by the user
    """

    MARKET_ON_CLOSE = "MARKET_ON_CLOSE"
    """
    Put the order into the auction (SP) at turn-in-play
    """


class InstructionReportStatus(str, Enum):

    SUCCESS = "SUCCESS"
    """
    The instruction was successful.
    """

    FAILURE = "FAILURE"
    """
    The instruction failed.
    """

    TIMEOUT = "TIMEOUT"
    """
    The order timed out & the status of the bet is unknown.  If a TIMEOUT error occurs on a placeOrders/replaceOrders request, you should check listCurrentOrders to verify the status of your bets before placing further orders. Please Note: Timeouts will occur after 5 seconds of attempting to process the bet but please allow up to 15 seconds for a timed out order to appear. After this time any unprocessed bets will automatically be Lapsed and no longer be available on the Exchange.
    """


class InstructionReportErrorCode(str, Enum):
    INVALID_BET_SIZE = "INVALID_BET_SIZE"
    """
    bet size is invalid for your currency or your regulator
    """

    INVALID_RUNNER = "INVALID_RUNNER"
    """
    Runner does not exist, includes vacant traps in greyhound racing
    """

    BET_TAKEN_OR_LAPSED = "BET_TAKEN_OR_LAPSED"
    """
    Bet cannot be cancelled or modified as it has already been taken or has been cancelled/lapsed Includes attempts to cancel/modify market on close BSP bets and cancelling limit on close BSP bets. The error may be returned on placeOrders request if for example a bet is placed at the point when a market admin event takes place (i.e. market is turned in-play).
    The error will also be returned if a market version is submitted and a material change has taken place since the bet was submitted causing the bet to be rejected.
    """

    BET_IN_PROGRESS = "BET_IN_PROGRESS"
    """
    No result was received from the matcher in a timeout configured for the system
    """

    RUNNER_REMOVED = "RUNNER_REMOVED"
    """
    Runner has been removed from the event
    """

    MARKET_NOT_OPEN_FOR_BETTING = "MARKET_NOT_OPEN_FOR_BETTING"
    """
    Attempt to edit a bet on a market that has closed.
    """

    LOSS_LIMIT_EXCEEDED = "LOSS_LIMIT_EXCEEDED"
    """
    The action has caused the account to exceed the self imposed loss limit
    """

    MARKET_NOT_OPEN_FOR_BSP_BETTING = "MARKET_NOT_OPEN_FOR_BSP_BETTING"
    """
    Market now closed to bsp betting. Turned in-play or has been reconciled
    """

    INVALID_PRICE_EDIT = "INVALID_PRICE_EDIT"
    """
    Attempt to edit down the price of a bsp limit on close lay bet, or edit up the price of a limit on close back bet
    """

    INVALID_ODDS = "INVALID_ODDS"
    """
    Odds not on price ladder - either edit or placement
    """

    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    """
    Insufficient funds available to cover the bet action. Either the exposure limit or available to bet limit would be exceeded
    """

    INVALID_PERSISTENCE_TYPE = "INVALID_PERSISTENCE_TYPE"
    """
    Invalid persistence type for this market, e.g. KEEP for a non in-play market.
    """

    ERROR_IN_MATCHER = "ERROR_IN_MATCHER"
    """
    A problem with the matcher prevented this action completing successfully
    """

    INVALID_BACK_LAY_COMBINATION = "INVALID_BACK_LAY_COMBINATION"
    """
    The order contains a back and a lay for the same runner at overlapping prices. This would guarantee a self match. This also applies to BSP limit on close bets
    """

    ERROR_IN_ORDER = "ERROR_IN_ORDER"
    """
    The action failed because the parent order failed
    """

    INVALID_BID_TYPE = "INVALID_BID_TYPE"
    """
    Bid type is mandatory
    """

    INVALID_BET_ID = "INVALID_BET_ID"
    """
    Bet for id supplied has not been found
    """

    CANCELLED_NOT_PLACED = "CANCELLED_NOT_PLACED"
    """
    Bet cancelled but replacement bet was not placed
    """

    RELATED_ACTION_FAILED = "RELATED_ACTION_FAILED"
    """
    Action failed due to the failure of a action on which this action is dependent
    """

    NO_ACTION_REQUIRED = "NO_ACTION_REQUIRED"
    """
    the action does not result in any state change. eg changing a persistence to it's current value
    """

    TIME_IN_FORCE_CONFLICT = "TIME_IN_FORCE_CONFLICT"
    """
    You may only specify a time in force on either the place request OR on individual limit order instructions (not both),
    since the implied behaviors are incompatible.
    """

    UNEXPECTED_PERSISTENCE_TYPE = "UNEXPECTED_PERSISTENCE_TYPE"
    """
    You have specified a persistence type for a FILL_OR_KILL order, which is nonsensical because no umatched portion
    can remain after the order has been placed.
    """

    INVALID_ORDER_TYPE = "INVALID_ORDER_TYPE"
    """
    You have specified a time in force of FILL_OR_KILL, but have included a non-LIMIT order type.
    """

    UNEXPECTED_MIN_FILL_SIZE = "UNEXPECTED_MIN_FILL_SIZE"
    """
    You have specified a minFillSize on a limit order, where the limit order's time in force is not FILL_OR_KILL.
    Using minFillSize is not supported where the time in force of the request (as opposed to an order) is FILL_OR_KILL.
    """

    INVALID_CUSTOMER_ORDER_REF = "INVALID_CUSTOMER_ORDER_REF"
    """
    The supplied customer order reference is too long.
    """

    INVALID_MIN_FILL_SIZE = "INVALID_MIN_FILL_SIZE"
    """
    The minFillSize must be greater than zero and less than or equal to the order's size.
    The minFillSize cannot be less than the minimum bet size for your currency
    """

    BET_LAPSED_PRICE_IMPROVEMENT_TOO_LARGE = "BET_LAPSED_PRICE_IMPROVEMENT_TOO_LARGE"
    """
    Your bet is lapsed. There is better odds than requested available in the market, but your
    preferences don't allow the system to match your bet against better odds. Change your betting
    preferences to accept better odds if you don't want to receive this error. Please see https://support.betfair.com/app/answers/detail/a_id/404/ for more details regarding Best Execution and how to update your settings.
    """


class GroupBy(str, Enum):
    EVENT_TYPE = "EVENT_TYPE"
    """
    A roll up of settled P&L, commission paid and number of bet orders, on a specified event type
    """
    EVENT = "EVENT"
    """
    A roll up of settled P&L, commission paid and number of bet orders, on a specified event
    """
    MARKET = "MARKET"
    """
    A roll up of settled P&L, commission paid and number of bet orders, on a specified market
    """
    SIDE = "SIDE"
    """
    An averaged roll up of settled P&L, and number of bets, on the specified side of a specified selection within a specified market, that are either settled or voided
    """
    BET = "BET"
    """
    The P&L, side and regulatory information etc, about each individual bet order.
    """


class BetStatus(str, Enum):

    SETTLED = "SETTLED"
    """
    A matched bet that was settled normally
    """
    VOIDED = "VOIDED"
    """
    A matched bet that was subsequently voided by Betfair, before, during or after settlement
    """
    LAPSED = "LAPSED"
    """
    Unmatched bet that was cancelled by Betfair (for example at turn in play).
    """
    CANCELLED = "CANCELLED"
    """
    Unmatched bet that was cancelled by an explicit customer action.
    """


class TimeInForce(str, Enum):

    FILL_OR_KILL = "FILL_OR_KILL"
    """
    Execute the transaction immediately and completely (filled to size or between minFillSize and size) or not at all (cancelled).

    For LINE markets Volume Weighted Average Price (VWAP) functionality is disabled
    """


class BetTargetType(str, Enum):

    BACKERS_PROFIT = "BACKERS_PROFIT"
    """
    The payout requested minus the calculated size at which this LimitOrder is to be placed. BetTargetType bets are invalid for LINE markets
    """
    PAYOUT = "PAYOUT"
    """
    The total payout requested on a LimitOrder
    """


class PriceLadderType(str, Enum):

    CLASSIC = "CLASSIC"
    """
    Price ladder increments traditionally used for Odds Markets.
    """

    FINEST = "FINEST"
    """
    Price ladder with the finest available increment, traditionally used for
    Asian Handicap markets.
    """

    LINE_RANGE = "LINE_RANGE"
    """
    Price ladder used for LINE markets. Refer to MarketLineRangeInfo for more details.
    """


class Betting(BaseEndpoint):
    """
    Betting operations.
    """

    URI = "SportsAPING/v1.0/"

    def list_event_types(
        self,
        filter: dict = market_filter(),
        locale: Optional[str] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[list, List[resources.EventTypeResult]]:
        """
        Returns a list of Event Types (i.e. Sports) associated with the markets
        selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.EventTypeResult]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listEventTypes")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json,
            resources.EventTypeResult,
            elapsed_time,
            lightweight,
        )

    def list_competitions(
        self,
        filter: dict = market_filter(),
        locale: Optional[str] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[list, List[resources.CompetitionResult]]:
        """
        Returns a list of Competitions (i.e., World Cup 2013) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.CompetitionResult]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listCompetitions")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json,
            resources.CompetitionResult,
            elapsed_time,
            lightweight,
        )

    def list_time_ranges(
        self,
        filter: dict = market_filter(),
        granularity: str = "DAYS",
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[list, List[resources.TimeRangeResult]]:
        """
        Returns a list of time ranges in the granularity specified in the
        request (i.e. 3PM to 4PM, Aug 14th to Aug 15th) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str granularity: The granularity of time periods that correspond
        to markets selected by the market filter
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.TimeRangeResult]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listTimeRanges")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json,
            resources.TimeRangeResult,
            elapsed_time,
            lightweight,
        )

    def list_events(
        self,
        filter: dict = market_filter(),
        locale: Optional[str] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[list, List[resources.EventResult]]:
        """
        Returns a list of Events (i.e, Reading vs. Man United) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.EventResult]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listEvents")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.EventResult, elapsed_time, lightweight
        )

    def list_market_types(
        self,
        filter: dict = market_filter(),
        locale: Optional[str] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[list, List[resources.MarketTypeResult]]:
        """
        Returns a list of market types (i.e. MATCH_ODDS, NEXT_GOAL) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.MarketTypeResult]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listMarketTypes")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json,
            resources.MarketTypeResult,
            elapsed_time,
            lightweight,
        )

    def list_countries(
        self,
        filter: dict = market_filter(),
        locale: Optional[str] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[list, List[resources.CountryResult]]:
        """
        Returns a list of Countries associated with the markets selected by
        the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.CountryResult]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listCountries")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.CountryResult, elapsed_time, lightweight
        )

    def list_venues(
        self,
        filter: dict = market_filter(),
        locale: Optional[str] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[list, List[resources.VenueResult]]:
        """
        Returns a list of Venues (i.e. Cheltenham, Ascot) associated with
        the markets selected by the MarketFilter.

        :param dict filter: The filter to select desired markets
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.VenueResult]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listVenues")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.VenueResult, elapsed_time, lightweight
        )

    def list_market_catalogue(
        self,
        filter: dict = market_filter(),
        market_projection: Optional[list] = None,
        sort: Optional[str] = None,
        max_results: int = 1,
        locale: Optional[str] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[list, List[resources.MarketCatalogue]]:
        """
        Returns a list of information about published (ACTIVE/SUSPENDED) markets
        that does not change (or changes very rarely).

        :param dict filter: The filter to select desired markets
        :param list market_projection: The type and amount of data returned about the market
        :param str sort: The order of the results
        :param int max_results: Limit on the total number of results returned, must be greater
        than 0 and less than or equal to 10000
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.MarketCatalogue]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listMarketCatalogue")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json,
            resources.MarketCatalogue,
            elapsed_time,
            lightweight,
        )

    def list_market_book(
        self,
        market_ids: list,
        price_projection: Optional[dict] = None,
        order_projection: Optional[str] = None,
        match_projection: Optional[str] = None,
        include_overall_position: Optional[bool] = None,
        partition_matched_by_strategy_ref: Optional[bool] = None,
        customer_strategy_refs: Optional[list] = None,
        currency_code: Optional[str] = None,
        matched_since: Optional[str] = None,
        bet_ids: Optional[list] = None,
        locale: Optional[str] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[list, List[resources.MarketBook]]:
        """
        Returns a list of dynamic data about markets. Dynamic data includes prices,
        the status of the market, the status of selections, the traded volume, and
        the status of any orders you have placed in the market

        :param list market_ids: One or more market ids
        :param dict price_projection: The projection of price data you want to receive in the response
        :param str order_projection: The orders you want to receive in the response
        :param str match_projection: If you ask for orders, specifies the representation of matches
        :param bool include_overall_position: If you ask for orders, returns matches for each selection
        :param bool partition_matched_by_strategy_ref: If you ask for orders, returns the breakdown of matches
        by strategy for each selection
        :param list customer_strategy_refs: If you ask for orders, restricts the results to orders matching
        any of the specified set of customer defined strategies
        :param str currency_code: A Betfair standard currency code
        :param str matched_since: If you ask for orders, restricts the results to orders that have at
        least one fragment matched since the specified date
        :param list bet_ids: If you ask for orders, restricts the results to orders with the specified bet IDs
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.MarketBook]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listMarketBook")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.MarketBook, elapsed_time, lightweight
        )

    def list_runner_book(
        self,
        market_id: str,
        selection_id: int,
        handicap: Optional[float] = None,
        price_projection: Optional[dict] = None,
        order_projection: Optional[str] = None,
        match_projection: Optional[str] = None,
        include_overall_position: Optional[bool] = None,
        partition_matched_by_strategy_ref: Optional[bool] = None,
        customer_strategy_refs: Optional[list] = None,
        currency_code: Optional[str] = None,
        matched_since: Optional[str] = None,
        bet_ids: Optional[list] = None,
        locale: Optional[str] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[list, List[resources.MarketBook]]:
        """
        Returns a list of dynamic data about a market and a specified runner.
        Dynamic data includes prices, the status of the market, the status of selections,
        the traded volume, and the status of any orders you have placed in the market

        :param unicode market_id: The unique id for the market
        :param int selection_id: The unique id for the selection in the market
        :param double handicap: The projection of price data you want to receive in the response
        :param dict price_projection: The projection of price data you want to receive in the response
        :param str order_projection: The orders you want to receive in the response
        :param str match_projection: If you ask for orders, specifies the representation of matches
        :param bool include_overall_position: If you ask for orders, returns matches for each selection
        :param bool partition_matched_by_strategy_ref: If you ask for orders, returns the breakdown of matches
        by strategy for each selection
        :param list customer_strategy_refs: If you ask for orders, restricts the results to orders matching
        any of the specified set of customer defined strategies
        :param str currency_code: A Betfair standard currency code
        :param str matched_since: If you ask for orders, restricts the results to orders that have at
        least one fragment matched since the specified date
        :param list bet_ids: If you ask for orders, restricts the results to orders with the specified bet IDs
        :param str locale: The language used for the response
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.MarketBook]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listRunnerBook")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json,
            resources.MarketBook,
            elapsed_time,
            lightweight,  # todo MarketBook?
        )

    def list_current_orders(
        self,
        bet_ids: Optional[list] = None,
        market_ids: Optional[list] = None,
        order_projection: Optional[str] = None,
        customer_order_refs: Optional[list] = None,
        customer_strategy_refs: Optional[list] = None,
        date_range: dict = time_range(),
        order_by: Optional[str] = None,
        sort_dir: Optional[str] = None,
        from_record: Optional[int] = None,
        record_count: Optional[int] = None,
        include_item_description: Optional[bool] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[dict, resources.CurrentOrders]:
        """
        Returns a list of your current orders.

        :param list bet_ids: If you ask for orders, restricts the results to orders with the specified bet IDs
        :param list market_ids: One or more market ids
        :param str order_projection: Optionally restricts the results to the specified order status
        :param list customer_order_refs: Optionally restricts the results to the specified customer order references
        :param list customer_strategy_refs: Optionally restricts the results to the specified customer strategy
        references
        :param dict date_range: Optionally restricts the results to be from/to the specified date, these dates
        are contextual to the orders being returned and therefore the dates used to filter on will change
        to placed, matched, voided or settled dates depending on the orderBy
        :param str order_by: Specifies how the results will be ordered. If no value is passed in, it defaults to BY_BET
        :param str sort_dir: Specifies the direction the results will be sorted in
        :param int from_record: Specifies the first record that will be returned
        :param int record_count: Specifies how many records will be returned from the index position 'fromRecord'
        :param bool include_item_description: If true then extra description parameters are included in the CurrentOrderSummaryReport
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.CurrentOrders
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listCurrentOrders")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.CurrentOrders, elapsed_time, lightweight
        )

    def list_cleared_orders(
        self,
        bet_status: str = "SETTLED",
        event_type_ids: Optional[list] = None,
        event_ids: Optional[list] = None,
        market_ids: Optional[list] = None,
        runner_ids: Optional[list] = None,
        bet_ids: Optional[list] = None,
        customer_order_refs: Optional[list] = None,
        customer_strategy_refs: Optional[list] = None,
        side: Optional[str] = None,
        settled_date_range: dict = time_range(),
        group_by: Optional[str] = None,
        include_item_description: Optional[bool] = None,
        locale: Optional[str] = None,
        from_record: Optional[int] = None,
        record_count: Optional[int] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[dict, resources.ClearedOrders]:
        """
        Returns a list of settled bets based on the bet status,
        ordered by settled date.

        :param str bet_status: Restricts the results to the specified status
        :param list event_type_ids: Optionally restricts the results to the specified Event Type IDs
        :param list event_ids: Optionally restricts the results to the specified Event IDs
        :param list market_ids: Optionally restricts the results to the specified market IDs
        :param list runner_ids: Optionally restricts the results to the specified Runners
        :param list bet_ids: If you ask for orders, restricts the results to orders with the specified bet IDs
        :param list customer_order_refs: Optionally restricts the results to the specified customer order references
        :param list customer_strategy_refs: Optionally restricts the results to the specified customer strategy
        references
        :param str side: Optionally restricts the results to the specified side
        :param dict settled_date_range: Optionally restricts the results to be from/to the specified settled date
        :param str group_by: How to aggregate the lines, if not supplied then the lowest level is returned
        :param bool include_item_description: If true then an ItemDescription object is included in the response
        :param str locale: The language used for the response
        :param int from_record: Specifies the first record that will be returned
        :param int record_count: Specifies how many records will be returned from the index position 'fromRecord'
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.ClearedOrders
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listClearedOrders")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.ClearedOrders, elapsed_time, lightweight
        )

    def list_market_profit_and_loss(
        self,
        market_ids: list,
        include_settled_bets: Optional[bool] = None,
        include_bsp_bets: Optional[bool] = None,
        net_of_commission: Optional[bool] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[list, List[resources.MarketProfitLoss]]:
        """
        Retrieve profit and loss for a given list of OPEN markets.

        :param list market_ids: List of markets to calculate profit and loss
        :param bool include_settled_bets: Option to include settled bets (partially settled markets only)
        :param bool include_bsp_bets: Option to include BSP bets
        :param bool net_of_commission: Option to return profit and loss net of users current commission
        rate for this market including any special tariffs
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: list[resources.MarketProfitLoss]
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "listMarketProfitAndLoss")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json,
            resources.MarketProfitLoss,
            elapsed_time,
            lightweight,
        )

    def place_orders(
        self,
        market_id: str,
        instructions: list,
        customer_ref: Optional[str] = None,
        market_version: Optional[dict] = None,
        customer_strategy_ref: Optional[str] = None,
        async_: Optional[bool] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[dict, resources.PlaceOrders]:
        """
        Place new orders into market.

        :param str market_id: The market id these orders are to be placed on
        :param list instructions: The number of place instructions
        :param str customer_ref: Optional parameter allowing the client to pass a unique string
        (up to 32 chars) that is used to de-dupe mistaken re-submissions
        :param dict market_version: Optional parameter allowing the client to specify which
        version of the market the orders should be placed on, e.g. "{'version': 123456}"
        :param str customer_strategy_ref: An optional reference customers can use to specify
        which strategy has sent the order
        :param bool async_: An optional flag (not setting equates to false) which specifies if
        the orders should be placed asynchronously
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.PlaceOrders
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "placeOrders")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.PlaceOrders, elapsed_time, lightweight
        )

    def cancel_orders(
        self,
        market_id: str = None,
        instructions: Optional[list] = None,
        customer_ref: Optional[str] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[dict, resources.CancelOrders]:
        """
        Cancel all bets OR cancel all bets on a market OR fully or partially
        cancel particular orders on a market.

        :param str market_id: If marketId and betId aren't supplied all bets are cancelled
        :param list instructions: All instructions need to be on the same market
        :param str customer_ref: Optional parameter allowing the client to pass a unique
        string (up to 32 chars) that is used to de-dupe mistaken re-submissions
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.CancelOrders
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "cancelOrders")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.CancelOrders, elapsed_time, lightweight
        )

    def update_orders(
        self,
        market_id: Optional[str] = None,
        instructions: Optional[list] = None,
        customer_ref: Optional[str] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[dict, resources.UpdateOrders]:
        """
        Update non-exposure changing field.

        :param str market_id: The market id these orders are to be placed on
        :param list instructions: The update instructions
        :param str customer_ref: Optional parameter allowing the client to pass a unique
        string (up to 32 chars) that is used to de-dupe mistaken re-submissions
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.UpdateOrders
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "updateOrders")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.UpdateOrders, elapsed_time, lightweight
        )

    def replace_orders(
        self,
        market_id: str,
        instructions: list,
        customer_ref: Optional[str] = None,
        market_version: Optional[dict] = None,
        async_: Optional[bool] = None,
        session: Optional[requests.Session] = None,
        lightweight: Optional[bool] = None,
    ) -> Union[dict, resources.ReplaceOrders]:
        """
        This operation is logically a bulk cancel followed by a bulk place.
        The cancel is completed first then the new orders are placed.

        :param str market_id: The market id these orders are to be placed on
        :param list instructions: The number of replace instructions.  The limit
        of replace instructions per request is 60
        :param str customer_ref: Optional parameter allowing the client to pass a unique
        string (up to 32 chars) that is used to de-dupe mistaken re-submissions
        :param dict market_version: Optional parameter allowing the client to specify
        which version of the market the orders should be placed on, e.g. "{'version': 123456}"
        :param bool async_: An optional flag (not setting equates to false) which specifies
        if the orders should be replaced asynchronously
        :param requests.session session: Requests session object
        :param bool lightweight: If True will return dict not a resource

        :rtype: resources.ReplaceOrders
        """
        params = clean_locals(locals())
        method = "%s%s" % (self.URI, "replaceOrders")
        (response, response_json, elapsed_time) = self.request(method, params, session)
        return self.process_response(
            response_json, resources.ReplaceOrders, elapsed_time, lightweight
        )
