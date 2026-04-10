{% set source_model = source('ecommerce', 'raw_olist_customers_dataset') -%}

with
    base as (
        select
            customer_id as id
            , customer_unique_id as unique_id
            , customer_zip_code_prefix as zip_code_prefix
            , customer_city as city
            , customer_state as state
        from
            {{ source_model }}
    )

select * from base
