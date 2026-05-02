with
    orders as (
        select * from {{ ref('stg_ecom_orders') }}
        where status = 'delivered'
    )

    , customers as (
        select * from {{ ref('stg_ecom_customers') }}
    )

    , items as (
        select * from {{ ref('int_order_items_aggregated') }}
    )

    , geo as (
        select * from {{ ref('int_geolocation_cleaned') }}
    )

    , combined as (
        select
            orders.order_id
            , customers.unique_id as customer_unique_id
            , customers.zip_code_prefix
            , customers.city
            , customers.state
            , geo.lat
            , geo.lng
            , coalesce(items.total_freight_amount, 0) as total_freight_amount
            , coalesce(items.total_order_amount, 0) as total_order_amount
            , cast(orders.purchase_timestamp as date) as order_date
            , date_diff('day', cast(orders.purchase_timestamp as date), cast(orders.delivered_customer_timestamp as date)) as delivery_time_days
        from
            orders
        left join customers
            on orders.customer_id = customers.id 
        inner join geo
            using(zip_code_prefix)
        left join items
            using(order_id)   
    )

select * from combined
