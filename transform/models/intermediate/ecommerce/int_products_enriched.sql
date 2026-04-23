with
    products as (
        select * from {{ ref('stg_ecom_products') }}
    )

    , category_names as (
        select * from {{ ref('stg_ecom_product_category_name_translation')}}
    )

    , combined as (
        select
            prds.* exclude (product_category_name)
            , ctgr.category_name_english
        from
            products as prds
        inner join category_names as ctgr
            on prds.product_category_name = ctgr.category_name
    )

select * from combined