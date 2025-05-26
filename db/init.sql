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
    username VARCHAR(255) NOT NULL,
    bio TEXT NULL,
    avatar VARCHAR(255) NULL,
    birthdate DATE NULL,
    fcm_token VARCHAR(255) NULL,
    user_uuid UUID NOT NULL REFERENCES "user"(uuid) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE collections (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    number_of_articles INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    profile_id INTEGER NOT NULL,
    FOREIGN KEY (profile_id) REFERENCES profile(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    photo VARCHAR(255),
    read_time_seconds INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    profile_id INTEGER NOT NULL,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (profile_id) REFERENCES profile(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE collection_articles(
    article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    collection_id INTEGER NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    PRIMARY KEY (article_id, collection_id)
);

CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE articles_categories (
    article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES category(id) ON DELETE CASCADE,
    PRIMARY KEY (article_id, category_id)
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
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
    article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (author_id, article_id)
);

CREATE TABLE report (
    id SERIAL PRIMARY KEY,
    article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
