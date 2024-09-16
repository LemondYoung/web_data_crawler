CREATE TABLE `s_url_manager` (
  `id` int NOT NULL AUTO_INCREMENT,
  `style_code` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '风格代码',
  `url` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '必填',
  `url_name` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '选填',
  `remark` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '备注',
  `url_type` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'url类型',
  `url_status` int DEFAULT '0' COMMENT 'url状态（初始化：0，解析成功：1，其他状态：2，解析失败：-1）',
  `source_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT 'douban' COMMENT '来源名称',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `url` (`url`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=19809 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='url管理表'