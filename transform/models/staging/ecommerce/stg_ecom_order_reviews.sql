{% set source_model = source('ecommerce', 'raw_olist_order_reviews_dataset') -%}

with
    base as (
        select
            review_id
            , order_id
            , review_score 
            , review_comment_title as comment_title
            , review_comment_message as comment_message
            , cast(review_creation_date as date) as creation_date
            , cast(review_answer_timestamp as timestamp) as answer_timestamp
        from
            {{ source_model }}
    )

select * from base
