{% set source_model = source('ecommerce', 'raw_olist_order_payments_dataset') -%}

with
    base as (
        select
            order_id 
            , payment_sequential
            , payment_type 
            , payment_installments
            , payment_value
        from
            {{ source_model }}
    )

select * from base
