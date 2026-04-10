{% set source_model = source('ecommerce', 'raw_olist_order_items_dataset') -%}

with
    base as (
        select
            order_id 
            , order_item_id
            , product_id 
            , seller_id
            , cast(shipping_limit_date as timestamp) as shipping_limit_at
            , price
            , freight_value
            , {{ dbt_utils.generate_surrogate_key([
                    'order_id', 
                    'order_item_id'
                ]) }} as order_item_sk
        from
            {{ source_model }}
    )

select * from base
