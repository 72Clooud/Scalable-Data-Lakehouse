{% set source_model = source('ecommerce', 'raw_product_category_name_translation') -%}

with
    base as (
        select
            product_category_name as category_name
            , product_category_name_english as category_name_english
        from
            {{ source_model }}
    )

select * from base
