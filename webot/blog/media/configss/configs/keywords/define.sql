-- 关键词数据库
-- 字段名称:
-- * name: 名称
-- * type: 类型(0:weibo-O, 1:b1, 2:b2, 3:weibo-T, 5:export-dig, 
-- *            6:secretary-dig, 7:topic-dig, 11:search-engine)
-- * priority: 优先级(1-2-3:低-中-高)
-- * created: 创建时间
-- * updated: 更新时间
-- * enabled: 是否可用(0:否, 1:是)

CREATE DATABASE IF NOT EXISTS keyword DEFAULT CHARSET=utf8;

USE keyword

CREATE TABLE IF NOT EXISTS keyword
(
    name VARCHAR(255) NOT NULL,
    type TINYINT NOT NULL,
    priority TINYINT NOT NULL,
    created DATETIME NOT NULL,
    updated DATETIME NOT NULL,
    enabled BOOLEAN NOT NULL,
    PRIMARY KEY (`name`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

