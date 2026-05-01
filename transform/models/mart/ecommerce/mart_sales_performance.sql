with
    items as (
        select * from {{ ref('int_order_items_aggregated') }}
    )

    , payments as (
        select * from {{ ref('int_order_payments_aggregated') }}
    )

    , orders as ( 
        select * from {{ ref('stg_ecom_orders') }}
        where status in ('delivered', 'shipped', 'invoiced', 'processing', 'approved')
    )

    , combined as (
        select
            cast(orders.purchase_timestamp as date) as order_date,
            count(distinct orders.order_id) as total_orders,
            sum(items.items_count) as total_items_sold,
            sum(items.total_products_amount) as total_revenue,
            sum(items.total_freight_amount) as total_freight_cost,
            sum(items.total_order_amount) as total_order_value,
            sum(payments.total_payment_amount) as total_payments_received
        from
            orders
        left join payments
            using(order_id)
        left join items
            using(order_id)
        group by 1
    )

    , kpi_calculation as (
        select
            *
            , case 
                when total_orders > 0 then total_order_value / total_orders 
                else 0 
            end as average_order_value
        from
            combined
    )

select * from kpi_calculation
