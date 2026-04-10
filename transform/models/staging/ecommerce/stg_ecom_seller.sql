{% set source_model = source('ecommerce', 'raw_olist_sellers_dataset') -%}

with
    base as (
        select
            seller_id
            , seller_zip_code_prefix as zip_code_prefix
            , seller_city as city
            , seller_state as state
        from
            {{ source_model }}
    )

select * from base
