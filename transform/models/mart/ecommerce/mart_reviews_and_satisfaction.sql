with
    reviews as (
        select * from {{ ref('stg_ecom_order_reviews') }}
    )

    , orders as (
        select * from {{ ref('stg_ecom_orders') }}
        where status = 'delivered'
    )

    , combined as (
        select  
            reviews.review_id
            , reviews.order_id
            , reviews.review_score
            , case
                when reviews.comment_message is not null
                    then true
                else false
            end as has_comment
            , cast(orders.purchase_timestamp as date) as order_date
            , date_diff('day', cast(orders.purchase_timestamp as date), cast(orders.delivered_customer_timestamp as date)) as delivery_time_days
            , case 
                when orders.delivered_customer_timestamp > orders.estimated_delivery_date 
                    then true 
                else false 
            end as is_late_delivery
        from reviews
        inner join orders
            on reviews.order_id = orders.order_id
    )

select * from combined
