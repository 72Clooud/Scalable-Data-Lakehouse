{% set source_model = source('ecommerce', 'raw_olist_geolocation_dataset') -%}

with
    base as (
        select
            geolocation_zip_code_prefix as zip_code_prefix
            , geolocation_lat as lat
            , geolocation_lng as lng
            , geolocation_city as city
            , geolocation_state as state
            , {{ dbt_utils.generate_surrogate_key([
                'geolocation_zip_code_prefix', 
                'geolocation_lat', 
                'geolocation_lng'
            ]) }} as geolocation_id
        from
            {{ source_model }}
    )

select * from base
