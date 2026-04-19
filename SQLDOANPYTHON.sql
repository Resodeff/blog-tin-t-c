-- =====================================================================
-- SCRIPT TẠO CƠ SỞ DỮ LIỆU BLOG (CHUYỂN TỪ DJANGO MODEL SANG SQL SERVER)
-- =====================================================================

-- 0. Tạo bảng User (Mô phỏng bảng auth_user mặc định của Django)
CREATE TABLE [auth_user] (
    [id] INT IDENTITY(1,1) PRIMARY KEY,
    [password] NVARCHAR(128) NOT NULL,
    [last_login] DATETIME2 NULL,
    [is_superuser] BIT NOT NULL DEFAULT 0,
    [username] NVARCHAR(150) NOT NULL UNIQUE,
    [first_name] NVARCHAR(150) NOT NULL DEFAULT '',
    [last_name] NVARCHAR(150) NOT NULL DEFAULT '',
    [email] NVARCHAR(254) NOT NULL DEFAULT '',
    [is_staff] BIT NOT NULL DEFAULT 0,
    [is_active] BIT NOT NULL DEFAULT 1,
    [date_joined] DATETIME2 NOT NULL DEFAULT GETDATE()
);

-- 1. Tạo bảng Danh mục (CATEGORY)
CREATE TABLE [CATEGORY] (
    [ID] INT IDENTITY(1,1) PRIMARY KEY,
    [NAME] NVARCHAR(100) NOT NULL
);

-- 2. Tạo bảng Thẻ (TAG)
CREATE TABLE [TAG] (
    [ID] INT IDENTITY(1,1) PRIMARY KEY,
    [NAME] NVARCHAR(50) NOT NULL
);

-- 3. Tạo bảng Bài viết (POST)
CREATE TABLE [POST] (
    [ID] INT IDENTITY(1,1) PRIMARY KEY,
    [TITLE] NVARCHAR(200) NOT NULL,
    [CONTENT] NVARCHAR(MAX) NOT NULL,
    [HINHANH] NVARCHAR(100) NULL, -- Lưu đường dẫn file ảnh
    [NGAYDANG] DATETIME2 DEFAULT GETDATE(),
    [NGAYSUA] DATETIME2 DEFAULT GETDATE(),
    
    -- Khóa ngoại Tác giả (Tham chiếu bảng User)
    [TACGIA_ID] INT NOT NULL,
    CONSTRAINT FK_POST_USER FOREIGN KEY ([TACGIA_ID]) 
        REFERENCES [auth_user]([id]) ON DELETE CASCADE,

    -- Khóa ngoại Danh mục
    [BAIVIET_ID] INT NULL,
    CONSTRAINT FK_POST_CATEGORY FOREIGN KEY ([BAIVIET_ID]) 
        REFERENCES [CATEGORY]([ID]) ON DELETE SET NULL
);

-- 4. Tạo bảng trung gian cho quan hệ ManyToMany giữa POST và TAG
CREATE TABLE [POST_THELOAI] (
    [ID] INT IDENTITY(1,1) PRIMARY KEY,
    [POST_ID] INT NOT NULL,
    [TAG_ID] INT NOT NULL,
    CONSTRAINT FK_POSTTAG_POST FOREIGN KEY ([POST_ID]) 
        REFERENCES [POST]([ID]) ON DELETE CASCADE,
    CONSTRAINT FK_POSTTAG_TAG FOREIGN KEY ([TAG_ID]) 
        REFERENCES [TAG]([ID]) ON DELETE CASCADE
);

-- 5. Tạo bảng Bình luận (COMMENT)
CREATE TABLE [COMMENT] (
    [ID] INT IDENTITY(1,1) PRIMARY KEY,
    [NOIDUNG] NVARCHAR(MAX) NOT NULL,
    [NGAYBINHLUAN] DATETIME2 DEFAULT GETDATE(),

    -- Khóa ngoại tới Bài viết (Xóa bài viết -> Xóa bình luận)
    [THONGTIN_ID] INT NOT NULL,
    CONSTRAINT FK_COMMENT_POST FOREIGN KEY ([THONGTIN_ID]) 
        REFERENCES [POST]([ID]) ON DELETE CASCADE,

    -- Khóa ngoại tới Người bình luận (Sử dụng NO ACTION để tránh lỗi multiple cascade paths)
    [NGUOIBINHLUAN_ID] INT NOT NULL,
    CONSTRAINT FK_COMMENT_USER FOREIGN KEY ([NGUOIBINHLUAN_ID]) 
        REFERENCES [auth_user]([id]) ON DELETE NO ACTION 
);