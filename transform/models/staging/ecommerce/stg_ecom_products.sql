{% set source_model = source('ecommerce', 'raw_olist_products_dataset') -%}

with
    base as (
        select
            product_id as id
            , product_category_name
            , product_name_lenght
            , product_description_lenght as description_lenght
            , product_photos_qty as photos_qty
            , product_weight_g as weight_g
            , product_length_cm as length_cm
            , product_height_cm as height_cm
            , product_width_cm as width_cm
        from
            {{ source_model }}
    )

select * from base
