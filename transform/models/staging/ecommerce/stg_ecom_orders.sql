{% set source_model = source('ecommerce', 'raw_olist_orders_dataset') -%}

with
    base as (
        select
            order_id
            , customer_id
            , order_status as status 
            , cast(order_purchase_timestamp as timestamp) as purchase_timestamp
            , cast(order_approved_at as timestamp) as approved_at
            , cast(order_delivered_carrier_date as date) as delivered_carrier_date
            , cast(order_delivered_customer_date as timestamp) as delivered_customer_timestamp
            , cast(order_estimated_delivery_date as date) as estimated_delivery_date
        from
            {{ source_model }}
    )

select * from base
