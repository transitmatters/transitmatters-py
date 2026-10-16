"""Contains all the data models used in inputs/outputs"""

from .aggregate_by_date import AggregateByDate
from .aggregate_by_time import AggregateByTime
from .aggregate_dwells_params import AggregateDwellsParams
from .aggregate_headways_params import AggregateHeadwaysParams
from .aggregate_travel_times_params import AggregateTravelTimesParams
from .alert import Alert
from .alert_active_period import AlertActivePeriod
from .alert_delays_by_line_params import AlertDelaysByLineParams
from .alert_delays_by_line_params_agg import AlertDelaysByLineParamsAgg
from .alerts_by_date_params import AlertsByDateParams
from .by_day_kind_service_levels import ByDayKindServiceLevels
from .dashboard_line import DashboardLine
from .dashboard_line_ridershiphistory import DashboardLineRidershiphistory
from .dashboard_line_servicehistory import DashboardLineServicehistory
from .dashboard_service_day import DashboardServiceDay
from .dashboard_service_regime import DashboardServiceRegime
from .dashboard_service_regimes import DashboardServiceRegimes
from .dashboard_summary import DashboardSummary
from .dashboard_summary_totalridershiphistory import (
    DashboardSummaryTotalridershiphistory,
)
from .dashboard_summary_totalservicehistory import DashboardSummaryTotalservicehistory
from .dwell_event import DwellEvent
from .dwell_params import DwellParams
from .error_response import ErrorResponse
from .facilities_response import FacilitiesResponse
from .facilities_response_links import FacilitiesResponseLinks
from .facility import Facility
from .facility_attributes import FacilityAttributes
from .facility_links import FacilityLinks
from .facility_property import FacilityProperty
from .facility_relationships import FacilityRelationships
from .facility_stop_relationship import FacilityStopRelationship
from .get_line_delays_agg import GetLineDelaysAgg
from .get_scheduled_service_agg import GetScheduledServiceAgg
from .get_scheduled_service_response import GetScheduledServiceResponse
from .get_service_hours_agg import GetServiceHoursAgg
from .get_trip_metrics_agg import GetTripMetricsAgg
from .headway_aggregate_by_date import HeadwayAggregateByDate
from .headway_event import HeadwayEvent
from .headway_params import HeadwayParams
from .healthcheck_response import HealthcheckResponse
from .healthcheck_response_failed_checks import HealthcheckResponseFailedChecks
from .json_api_resource_identifier import JsonApiResourceIdentifier
from .json_api_version import JsonApiVersion
from .line_delay_entry import LineDelayEntry
from .live_alert import LiveAlert
from .ridership_entry import RidershipEntry
from .ridership_params import RidershipParams
from .route_not_found_response import RouteNotFoundResponse
from .routes_response import RoutesResponse
from .scheduled_service_count import ScheduledServiceCount
from .scheduled_service_params import ScheduledServiceParams
from .scheduled_service_params_agg import ScheduledServiceParamsAgg
from .service_hours_entry import ServiceHoursEntry
from .service_hours_params import ServiceHoursParams
from .service_hours_params_agg import ServiceHoursParamsAgg
from .service_levels_by_day_kind import ServiceLevelsByDayKind
from .service_ridership_dashboard_response import ServiceRidershipDashboardResponse
from .service_ridership_dashboard_response_linedata import (
    ServiceRidershipDashboardResponseLinedata,
)
from .service_ridership_dashboard_response_modedata import (
    ServiceRidershipDashboardResponseModedata,
)
from .speed_restriction_zone import SpeedRestrictionZone
from .speed_restrictions_params import SpeedRestrictionsParams
from .speed_restrictions_response import SpeedRestrictionsResponse
from .station_stop import StationStop
from .station_stop_stops import StationStopStops
from .stops_response import StopsResponse
from .stops_response_direction import StopsResponseDirection
from .time_prediction_bucket import TimePredictionBucket
from .time_prediction_params import TimePredictionParams
from .time_prediction_week import TimePredictionWeek
from .travel_time_aggregate_2_response import TravelTimeAggregate2Response
from .travel_time_event import TravelTimeEvent
from .travel_time_params import TravelTimeParams
from .trip_metrics_by_line_params import TripMetricsByLineParams
from .trip_metrics_by_line_params_agg import TripMetricsByLineParamsAgg
from .trip_metrics_entry import TripMetricsEntry

__all__ = (
    "AggregateByDate",
    "AggregateByTime",
    "AggregateDwellsParams",
    "AggregateHeadwaysParams",
    "AggregateTravelTimesParams",
    "Alert",
    "AlertActivePeriod",
    "AlertDelaysByLineParams",
    "AlertDelaysByLineParamsAgg",
    "AlertsByDateParams",
    "ByDayKindServiceLevels",
    "DashboardLine",
    "DashboardLineRidershiphistory",
    "DashboardLineServicehistory",
    "DashboardServiceDay",
    "DashboardServiceRegime",
    "DashboardServiceRegimes",
    "DashboardSummary",
    "DashboardSummaryTotalridershiphistory",
    "DashboardSummaryTotalservicehistory",
    "DwellEvent",
    "DwellParams",
    "ErrorResponse",
    "FacilitiesResponse",
    "FacilitiesResponseLinks",
    "Facility",
    "FacilityAttributes",
    "FacilityLinks",
    "FacilityProperty",
    "FacilityRelationships",
    "FacilityStopRelationship",
    "GetLineDelaysAgg",
    "GetScheduledServiceAgg",
    "GetScheduledServiceResponse",
    "GetServiceHoursAgg",
    "GetTripMetricsAgg",
    "HeadwayAggregateByDate",
    "HeadwayEvent",
    "HeadwayParams",
    "HealthcheckResponse",
    "HealthcheckResponseFailedChecks",
    "JsonApiResourceIdentifier",
    "JsonApiVersion",
    "LineDelayEntry",
    "LiveAlert",
    "RidershipEntry",
    "RidershipParams",
    "RouteNotFoundResponse",
    "RoutesResponse",
    "ScheduledServiceCount",
    "ScheduledServiceParams",
    "ScheduledServiceParamsAgg",
    "ServiceHoursEntry",
    "ServiceHoursParams",
    "ServiceHoursParamsAgg",
    "ServiceLevelsByDayKind",
    "ServiceRidershipDashboardResponse",
    "ServiceRidershipDashboardResponseLinedata",
    "ServiceRidershipDashboardResponseModedata",
    "SpeedRestrictionsParams",
    "SpeedRestrictionsResponse",
    "SpeedRestrictionZone",
    "StationStop",
    "StationStopStops",
    "StopsResponse",
    "StopsResponseDirection",
    "TimePredictionBucket",
    "TimePredictionParams",
    "TimePredictionWeek",
    "TravelTimeAggregate2Response",
    "TravelTimeEvent",
    "TravelTimeParams",
    "TripMetricsByLineParams",
    "TripMetricsByLineParamsAgg",
    "TripMetricsEntry",
)
