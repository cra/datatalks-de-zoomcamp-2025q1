{{ config(materialized='table') }}

with trips_data as (
    select
        service_type,
        sum(total_amount) as revenue,
        pu_year,
        pu_quarter
    from {{ ref('fact_trips') }}
    group by 1, 3, 4
)
select
    a.service_type,
    a.revenue,
    a.pu_year || '/' || a.pu_quarter as yearquarter,
    (a.revenue - b.revenue) / b.revenue as yoy_growth
from trips_data a
left join trips_data b on 1=1
    AND a.service_type = b.service_type
    AND a.pu_quarter = b.pu_quarter
    AND a.pu_year = b.pu_year + 1 

