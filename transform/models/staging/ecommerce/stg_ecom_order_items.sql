{% set source_model = source('ecommerce', 'raw_olist_order_items_dataset') -%}

with
    base as (
        select
            order_id 
            , order_item_id as item_id
            , product_id 
            , seller_id
            , cast(shipping_limit_date as timestamp) as shipping_limit_date 
            , price
            , freight_value
        from
            {{ source_model }}
    )

select * from base
