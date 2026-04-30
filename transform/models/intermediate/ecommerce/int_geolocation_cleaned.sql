with
    stg_model as (
        select * from {{ ref('stg_ecom_geolocation') }}
    )

    , cleaned as (
        select
            zip_code_prefix
            , avg(lat) as lat
            , avg(Ing) as lon
            , city
            , state
        from
            stg_model
        group by 
            zip_code_prefix, city, state
    )

select * from cleaned
