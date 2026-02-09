-- Miji Store: ตาราง profiles โยงกับ Supabase Auth (auth.users)
-- รันใน Supabase SQL Editor หลังเปิดใช้ Auth แล้ว

-- ตาราง profiles เก็บข้อมูลเพิ่มของ user (auth.users มีแค่ email/password)
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text,
  avatar_url text,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- เปิด RLS (Row Level Security)
alter table public.profiles enable row level security;

-- นโยบาย: user อ่าน/แก้ไขได้เฉพาะแถวของตัวเอง
create policy "Users can read own profile"
  on public.profiles for select
  using (auth.uid() = id);

create policy "Users can update own profile"
  on public.profiles for update
  using (auth.uid() = id);

-- Trigger: สร้าง profile อัตโนมัติเมื่อมี user ใหม่ใน auth.users
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, full_name, updated_at)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name'),
    now()
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

-- ลบ trigger เดิมถ้ามี แล้วสร้างใหม่
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- (Optional) แก้ไข updated_at อัตโนมัติ
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;
drop trigger if exists profiles_updated_at on public.profiles;
create trigger profiles_updated_at
  before update on public.profiles
  for each row execute function public.set_updated_at();
