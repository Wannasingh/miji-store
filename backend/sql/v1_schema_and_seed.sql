-- Miji Store Supabase Schema v1

-- Categories Table
create table if not exists categories (
  id bigint primary key generated always as identity,
  name text not null,
  slug text unique not null,
  description text,
  image_url text,
  created_at timestamp with time zone default now()
);

-- Products Table (Updated)
create table if not exists products (
  id bigint primary key generated always as identity,
  name text not null,
  description text,
  price decimal(10,2) not null,
  image_url text, -- Primary image
  category_id bigint references categories(id),
  is_new_arrival boolean default false,
  is_featured boolean default false,
  is_limited_edition boolean default false,
  created_at timestamp with time zone default now()
);

-- Product Images (Additional images)
create table if not exists product_images (
  id bigint primary key generated always as identity,
  product_id bigint references products(id) on delete cascade,
  image_url text not null,
  display_order int default 0
);

-- Product Variants (Sizes/Colors)
create table if not exists product_variants (
  id bigint primary key generated always as identity,
  product_id bigint references products(id) on delete cascade,
  color_name text,
  color_hex text,
  size text,
  stock_quantity int default 0,
  created_at timestamp with time zone default now()
);

-- Hero Banners
create table if not exists hero_banners (
  id bigint primary key generated always as identity,
  title text,
  subtitle text,
  button_text text,
  button_link text,
  image_url text,
  is_active boolean default true,
  created_at timestamp with time zone default now()
);

-- Newsletter Subscriptions
create table if not exists newsletter_subscriptions (
  id bigint primary key generated always as identity,
  email text unique not null,
  created_at timestamp with time zone default now()
);

-- Seed Data
insert into categories (name, slug) values 
('Apparel', 'apparel'),
('Accessories', 'accessories'),
('Objects', 'objects');

insert into products (name, description, price, image_url, category_id, is_new_arrival, is_limited_edition) values
('Premium Merino Polo', 'Crafted from exceptionally soft, 100% Australian Merino wool.', 125.00, 'https://lh3.googleusercontent.com/aida-public/AB6AXuC4FGw39OWITriYqfHjEfLGU0d-bfZRsha7Lf73IIv9FVvGyW1h7u5N-OiGdgvhfCEt64fnlhIh6tyTiknXed2uWP9kH77h3fcjOvspCi15GSMnSJwTrehmkUdZbtWOcWXXefkkdXoZxeWVSB67OO1lDtgOV1aQSWQFkMqRFFNJccQAPwBfDrsqSlXCi2UOOXoKSzIdf1Xed3XFzOBlEZdnUDpCVEOj-NUBZUrozVuRy1LS_6_4fPtL1lFG0ZSYYI154tsKYUqt7pmX', 1, true, true),
('Organic Cotton Tee', 'Essential / Cream White', 45.00, 'https://lh3.googleusercontent.com/aida-public/AB6AXuBR8-NIRGybcftnHVH3iAAswvvB0bqq3WB9m3f2chlxc9swOxlrpxG5tCM3KW-sub651sPvEM6NU0QrYVIjQLF5e93cPCPaGYsZ2AonEjpQUHi13mp2gbUhjJJaD45nHZ476d7fATRp89PE5pgPWVpjF6UZipGdPYa1KrS8UOb2p6fYnzvOGMk1Uzx1vGqUcF3TwV_tPziXiiJN1I69G7wruMMK8vHMoFZNct2R9i7W7gf--KCLwA9ReyR20i7qBk5AcQ3JLIPxxxkA', 1, true, false);

insert into product_variants (product_id, color_name, color_hex, size, stock_quantity) values
(1, 'Charcoal Grey', '#333333', 'S', 10),
(1, 'Charcoal Grey', '#333333', 'M', 15),
(2, 'Cream White', '#F6F6F8', 'L', 20);

insert into hero_banners (title, subtitle, button_text, button_link, image_url) values
('The Essence of Summer', 'Discover our curated collection of organic essentials designed for the modern lifestyle.', 'Shop New Arrivals', '/shop', 'https://lh3.googleusercontent.com/aida-public/AB6AXuD4JgrWpv1I9mqCpMbRVc5zXKDami4R-BWt2Qxbd1APr4rMz2tyh4fOQqf5oGmpexfrtpsIjHOzLsIFoYPKRm3vD93tUlHKr-Sc5coxRScACrkW-sAGpmFF5K7vZXq06rxPHpXybIV1Ivw0aQjqeFmzDne-fK1I-7wdMDQ1jalEEMwoRCedmgHXsdN8R3maEN5x0nKl1vIFVUqSNoQjw6IArZds_gp45c5AB4jnQ4ooirFveR0g2eHTK8DtV02D4bjwyF1Oot-lt4ca');
