# kuwo_music

## 酷我音乐数据采集

* 采集歌手

```bash
    $ python fetch_singers.py
```

* 采集歌曲元数据

```bash
    $ python fetch_music.py
```

* 下载音乐

```bash
    $ python download_music.py
```

## 数据库表设计

* singer

```sql
CREATE TABLE `singer` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `singer_id` int(10) NOT NULL DEFAULT '0',
  `singer_name` varchar(255) NOT NULL DEFAULT '',
  `fans_num` int(20) unsigned NOT NULL DEFAULT '0',
  `music_num` int(10) NOT NULL DEFAULT '0',
  `album_num` int(10) unsigned NOT NULL DEFAULT '0',
  `platform` int(5) unsigned NOT NULL DEFAULT '1' COMMENT '1: 酷我',
  `create_time` datetime NOT NULL,
  `modify_time` datetime NOT NULL,
  `extra` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_singerid_platform` (`singer_id`,`platform`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

* music

```sql
CREATE TABLE `music` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `sid` int(20) unsigned NOT NULL DEFAULT '0' COMMENT 'singer_id',
  `rid` int(20) unsigned NOT NULL DEFAULT '0',
  `artist` varchar(1000) NOT NULL DEFAULT '',
  `music_name` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT '歌曲名称',
  `album_name` varchar(255) NOT NULL DEFAULT '',
  `album_id` int(20) unsigned NOT NULL DEFAULT '0',
  `duration` int(10) unsigned NOT NULL DEFAULT '0',
  `pub_date` varchar(30) NOT NULL DEFAULT '' COMMENT 'releaseDate',
  `create_time` datetime NOT NULL,
  `modify_time` datetime NOT NULL,
  `extra` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_rid` (`rid`,`sid`) USING BTREE,
  KEY `idx_sid` (`sid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

* link

```sql
CREATE TABLE `link` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `sid` int(20) unsigned NOT NULL DEFAULT '0',
  `rid` int(20) unsigned NOT NULL DEFAULT '0',
  `mp3_url` varchar(500) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `create_time` datetime NOT NULL,
  `modify_time` datetime NOT NULL,
  `extra` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `downloaded` int(4) unsigned NOT NULL DEFAULT '0' COMMENT '0: undownloaded 1: downloaded',
  PRIMARY KEY (`id`),
  KEY `idx_rid` (`rid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

```
