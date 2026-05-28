with
    stg_model as (
        select * from {{ ref('stg_ecom_order_items') }}
    )

    , aggregated as (
        select
            order_id
            , count(order_item_id) as items_count
            , sum(price) as total_products_amount
            , sum(freight_value) as total_freight_amount
            , sum(price) + sum(freight_value) as total_order_amount
        from 
            stg_model
        group by
            order_id
    )

select * from aggregated
