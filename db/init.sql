CREATE TABLE "user" (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role VARCHAR(10) NOT NULL CHECK (role IN ('User', 'Admin', 'Moderator')),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    status VARCHAR(10) CHECK (status IN ('Active', 'Inactive', 'Banned')) DEFAULT 'Active',
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    bio TEXT,
    avatar VARCHAR(255) NULL,
    birthdate DATE,
    gender VARCHAR(8) CHECK (gender IN ('Female', 'Male'),
    fcm_token VARCHAR(255),
    user_uuid UUID NOT NULL REFERENCES "user"(uuid),
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES profile(id) ON DELETE CASCADE,
    title VARCHAR(255),
    content TEXT,
    visibility_type VARCHAR(20) DEFAULT 'Private' CHECK (visibility_type IN ('Private', 'Public', 'Followers Only')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_published BOOLEAN DEFAULT FALSE
);

CREATE TABLE post_media (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    file_path VARCHAR(255),
    "order" INTEGER
);

CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE post_categories (
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES category(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, category_id)
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES profile(id) ON DELETE CASCADE,
    parent_comment_id INTEGER REFERENCES comments(id) ON DELETE SET NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE follows (
    follower_id INTEGER NOT NULL REFERENCES profile(id) ON DELETE CASCADE,
    following_id INTEGER NOT NULL REFERENCES profile(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, following_id)
);

CREATE TABLE likes (
    author_id INTEGER NOT NULL REFERENCES profile(id) ON DELETE CASCADE,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (author_id, post_id)
);

CREATE TABLE report (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
