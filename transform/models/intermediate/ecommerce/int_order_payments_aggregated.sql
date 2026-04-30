with
    stg_model as (
        select * from {{ ref('stg_ecom_order_payments') }}
    )

    , aggregated as (
        select
            order_id
            , sum(payment_value) as total_payment_amount
            , count(payment_sequential) as payment_methods_count
            , max(payment_installments) as max_installments
            , string_agg(payment_type, ', ') as payment_types_used
        from 
            stg_model
        group by
            order_id 
    )

select * from aggregated
