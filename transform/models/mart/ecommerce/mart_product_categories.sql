with
    items as (
        select * from {{ ref('stg_ecom_order_items') }}
    )

    , orders as (
        select * from {{ ref('stg_ecom_orders') }}
        where status in ('delivered', 'shipped', 'invoiced', 'processing', 'approved')
    )

    , products as (
        select * from {{ ref('int_products_enriched') }}
    )

    , joined as (
        select
            cast(orders.purchase_timestamp as date) as order_date
            , coalesce(products.category_name_english, 'Unknown Category') as product_category
            , items.price
        from items 
        inner join orders
            using(order_id)
        left join products 
            on items.product_id = products.id
    )

    , aggregated as (
        select
            order_date
            , product_category
            , count(*) as items_sold_count
            , sum(price) as total_revenue
            , cast(avg(price) as decimal(10,2)) as average_item_price
        from joined
        group by 1, 2
    )

select * from aggregated