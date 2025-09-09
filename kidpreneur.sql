-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 09, 2025 at 05:14 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kidpreneur`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_customuser'),
(22, 'Can change user', 6, 'change_customuser'),
(23, 'Can delete user', 6, 'delete_customuser'),
(24, 'Can view user', 6, 'view_customuser'),
(25, 'Can add idea', 7, 'add_idea'),
(26, 'Can change idea', 7, 'change_idea'),
(27, 'Can delete idea', 7, 'delete_idea'),
(28, 'Can view idea', 7, 'view_idea'),
(29, 'Can add comment', 8, 'add_comment'),
(30, 'Can change comment', 8, 'change_comment'),
(31, 'Can delete comment', 8, 'delete_comment'),
(32, 'Can view comment', 8, 'view_comment'),
(33, 'Can add like', 9, 'add_like'),
(34, 'Can change like', 9, 'change_like'),
(35, 'Can delete like', 9, 'delete_like'),
(36, 'Can view like', 9, 'view_like'),
(37, 'Can add follow', 10, 'add_follow'),
(38, 'Can change follow', 10, 'change_follow'),
(39, 'Can delete follow', 10, 'delete_follow'),
(40, 'Can view follow', 10, 'view_follow'),
(41, 'Can add contact message', 11, 'add_contactmessage'),
(42, 'Can change contact message', 11, 'change_contactmessage'),
(43, 'Can delete contact message', 11, 'delete_contactmessage'),
(44, 'Can view contact message', 11, 'view_contactmessage'),
(45, 'Can add conversation', 12, 'add_conversation'),
(46, 'Can change conversation', 12, 'change_conversation'),
(47, 'Can delete conversation', 12, 'delete_conversation'),
(48, 'Can view conversation', 12, 'view_conversation'),
(49, 'Can add message', 13, 'add_message'),
(50, 'Can change message', 13, 'change_message'),
(51, 'Can delete message', 13, 'delete_message'),
(52, 'Can view message', 13, 'view_message'),
(53, 'Can add message report', 14, 'add_messagereport'),
(54, 'Can change message report', 14, 'change_messagereport'),
(55, 'Can delete message report', 14, 'delete_messagereport'),
(56, 'Can view message report', 14, 'view_messagereport'),
(57, 'Can add message reaction', 15, 'add_messagereaction'),
(58, 'Can change message reaction', 15, 'change_messagereaction'),
(59, 'Can delete message reaction', 15, 'delete_messagereaction'),
(60, 'Can view message reaction', 15, 'view_messagereaction'),
(61, 'Can add forum category', 16, 'add_forumcategory'),
(62, 'Can change forum category', 16, 'change_forumcategory'),
(63, 'Can delete forum category', 16, 'delete_forumcategory'),
(64, 'Can view forum category', 16, 'view_forumcategory'),
(65, 'Can add forum post', 17, 'add_forumpost'),
(66, 'Can change forum post', 17, 'change_forumpost'),
(67, 'Can delete forum post', 17, 'delete_forumpost'),
(68, 'Can view forum post', 17, 'view_forumpost'),
(69, 'Can add forum post comment', 18, 'add_forumpostcomment'),
(70, 'Can change forum post comment', 18, 'change_forumpostcomment'),
(71, 'Can delete forum post comment', 18, 'delete_forumpostcomment'),
(72, 'Can view forum post comment', 18, 'view_forumpostcomment'),
(73, 'Can add forum post report', 19, 'add_forumpostreport'),
(74, 'Can change forum post report', 19, 'change_forumpostreport'),
(75, 'Can delete forum post report', 19, 'delete_forumpostreport'),
(76, 'Can view forum post report', 19, 'view_forumpostreport'),
(77, 'Can add forum post comment like', 20, 'add_forumpostcommentlike'),
(78, 'Can change forum post comment like', 20, 'change_forumpostcommentlike'),
(79, 'Can delete forum post comment like', 20, 'delete_forumpostcommentlike'),
(80, 'Can view forum post comment like', 20, 'view_forumpostcommentlike'),
(81, 'Can add forum post like', 21, 'add_forumpostlike'),
(82, 'Can change forum post like', 21, 'change_forumpostlike'),
(83, 'Can delete forum post like', 21, 'delete_forumpostlike'),
(84, 'Can view forum post like', 21, 'view_forumpostlike'),
(85, 'Can add forum post comment report', 22, 'add_forumpostcommentreport'),
(86, 'Can change forum post comment report', 22, 'change_forumpostcommentreport'),
(87, 'Can delete forum post comment report', 22, 'delete_forumpostcommentreport'),
(88, 'Can view forum post comment report', 22, 'view_forumpostcommentreport');

-- --------------------------------------------------------

--
-- Table structure for table `conversation`
--

CREATE TABLE `conversation` (
  `id` bigint(20) NOT NULL,
  `subject` varchar(255) NOT NULL DEFAULT '(No Subject)',
  `user1_id` bigint(20) NOT NULL,
  `user2_id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `conversation`
--

INSERT INTO `conversation` (`id`, `subject`, `user1_id`, `user2_id`, `created_at`) VALUES
(2, 'Hi Savi', 2, 4, '2025-09-09 02:50:25.609338');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(8, 'ideas', 'comment'),
(11, 'ideas', 'contactmessage'),
(12, 'ideas', 'conversation'),
(6, 'ideas', 'customuser'),
(10, 'ideas', 'follow'),
(16, 'ideas', 'forumcategory'),
(17, 'ideas', 'forumpost'),
(18, 'ideas', 'forumpostcomment'),
(20, 'ideas', 'forumpostcommentlike'),
(22, 'ideas', 'forumpostcommentreport'),
(21, 'ideas', 'forumpostlike'),
(19, 'ideas', 'forumpostreport'),
(7, 'ideas', 'idea'),
(9, 'ideas', 'like'),
(13, 'ideas', 'message'),
(15, 'ideas', 'messagereaction'),
(14, 'ideas', 'messagereport'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-09-04 20:04:55.154256'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-09-04 20:04:55.182723'),
(3, 'auth', '0001_initial', '2025-09-04 20:04:55.302761'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-09-04 20:04:55.333294'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-09-04 20:04:55.339292'),
(6, 'auth', '0004_alter_user_username_opts', '2025-09-04 20:04:55.343288'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-09-04 20:04:55.346287'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-09-04 20:04:55.347289'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-09-04 20:04:55.353299'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-09-04 20:04:55.358286'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-09-04 20:04:55.362302'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-09-04 20:04:55.371115'),
(13, 'auth', '0011_update_proxy_permissions', '2025-09-04 20:04:55.377104'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-09-04 20:04:55.380104'),
(15, 'ideas', '0001_initial', '2025-09-04 20:04:56.343906'),
(16, 'admin', '0001_initial', '2025-09-04 20:04:56.432879'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-09-04 20:04:56.443874'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-09-04 20:04:56.449875'),
(19, 'sessions', '0001_initial', '2025-09-04 20:04:56.481717'),
(20, 'ideas', '0002_comment_created_at', '2025-09-04 20:09:58.602802'),
(21, 'ideas', '0003_idea_is_archived', '2025-09-04 21:05:06.817556'),
(22, 'ideas', '0002_alter_conversation_table', '2025-09-07 17:11:30.807793'),
(23, 'ideas', '0003_alter_message_options_message_attachment_and_more', '2025-09-07 17:17:12.673660'),
(24, 'ideas', '0004_alter_message_options_conversation_subject_and_more', '2025-09-07 17:21:48.274463'),
(25, 'ideas', '0005_alter_message_folder_delete_messagereaction', '2025-09-08 17:06:41.101651'),
(26, 'ideas', '0006_forumcategory_forumpost_forumpostcomment_and_more', '2025-09-08 17:48:07.060449'),
(27, 'ideas', '0007_forumpost_document_forumpost_image_and_more', '2025-09-08 17:53:38.381449'),
(28, 'ideas', '0008_remove_forumpostcommentreport_comment_and_more', '2025-09-08 18:15:09.926053'),
(29, 'ideas', '0009_remove_forumpost_created_at_alter_forumpost_category_and_more', '2025-09-08 18:19:19.658572'),
(30, 'ideas', '0010_forumpost_created_at', '2025-09-08 18:37:17.506343'),
(31, 'ideas', '0011_forumpost_slug', '2025-09-08 18:38:11.571173');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('5acko4nn21qbc8u2qiu4mvfcm3goafiw', '.eJxVjDkOwjAURO_iGll4kw0lPWew_mYcQI4UJ1XE3UmkFFDOvDezqgzLXPPSZcoDq6uy6vTbIdBL2g74Ce0xahrbPA2od0UftOv7yPK-He7fQYVet_U5IiTgSCGIj4SXYiRggOQwWBtdIhbyYgx4b5wtBYHdli1EoWST-nwB_kc4hQ:1uvoHz:xj-PC2H2ICM4JW47x13xc1B8BYWdyefsC3PZwcn9r8I', '2025-09-23 02:40:59.680965'),
('d7askd0y0c6j0jdgy0o66sark67txvsq', '.eJxVjDkOwjAURO_iGll4kw0lPWew_mYcQI4UJ1XE3UmkFFDOvDezqgzLXPPSZcoDq6uy6vTbIdBL2g74Ce0xahrbPA2od0UftOv7yPK-He7fQYVet_U5IiTgSCGIj4SXYiRggOQwWBtdIhbyYgx4b5wtBYHdli1EoWST-nwB_kc4hQ:1uvQxu:gH02m7BJZ-YMH74XrKLLrj_UHzWjfOdhKOKMkiWAgNM', '2025-09-22 01:46:42.993001'),
('d82v0lm78nkux2oeogdt6a0hn1fgokbo', '.eJxVjDkOwjAURO_iGll4kw0lPWew_mYcQI4UJ1XE3UmkFFDOvDezqgzLXPPSZcoDq6uy6vTbIdBL2g74Ce0xahrbPA2od0UftOv7yPK-He7fQYVet_U5IiTgSCGIj4SXYiRggOQwWBtdIhbyYgx4b5wtBYHdli1EoWST-nwB_kc4hQ:1uvJiu:DYK2lpX-lgC6C-2zpYe1FLCo_-jC6JIYrKuSe3SEbEc', '2025-09-21 18:02:44.227205'),
('fwo3g98ioodwebg5xxs7h9n9jyippl5b', '.eJxVjDkOwjAURO_iGll4kw0lPWew_mYcQI4UJ1XE3UmkFFDOvDezqgzLXPPSZcoDq6uy6vTbIdBL2g74Ce0xahrbPA2od0UftOv7yPK-He7fQYVet_U5IiTgSCGIj4SXYiRggOQwWBtdIhbyYgx4b5wtBYHdli1EoWST-nwB_kc4hQ:1uuS99:zvHUTkuZ6wzzJQKTjCYaxyhEpDAaQUou20PIKFXPh5o', '2025-09-19 08:50:15.508935'),
('mkl5jgtoobd3anf59zlwhrgn765enhbn', '.eJxVjEEOwiAQRe_C2hCYAqUu3XsGMgODVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3EWVpx-N8L44LqDdMd6azK2ui4zyV2RB-3y2hI_L4f7d1Cwl28N0UDknB2x8hohDaP1GkBRhNFk76eBs4qWQDM7MsYoJHTZO_STG7R4fwDrSzfN:1uvodr:ZaTDjBCMcOE5DrFQIaviN-khiocaK_mSvPd5DebVYt4', '2025-09-23 03:03:35.363731'),
('nzojuw4null6maoc4hitb1dnqq3iuzei', '.eJxVjEsOAiEQBe_C2hCg-YhL956BNE0rowaSYWZlvLtOMgvdvqp6L5FwXWpaB89pKuIkQBx-t4z04LaBcsd265J6W-Ypy02ROx3y0gs_z7v7d1Bx1G_tVEC2hN7pcC25qGgVs84OvYV8pEIRovHASMFbRAgAGIMmg9Yb68T7A_CvN8Y:1uvak7:GU8ij_LpDvdAKsZr6_YNyowJ444WjJu-WQSzb0rtjvI', '2025-09-22 12:13:07.272644'),
('pg049iknccq36fxvdpvjmbqpynof3a47', '.eJxVjEsOAiEQBe_C2hCg-YhL956BNE0rowaSYWZlvLtOMgvdvqp6L5FwXWpaB89pKuIkQBx-t4z04LaBcsd265J6W-Ypy02ROx3y0gs_z7v7d1Bx1G_tVEC2hN7pcC25qGgVs84OvYV8pEIRovHASMFbRAgAGIMmg9Yb68T7A_CvN8Y:1uvRO2:df9gXTiCl4NhaYJsRcBQXIj6GOPoNc92cqZIGQ91qoY', '2025-09-22 02:13:42.632982');

-- --------------------------------------------------------

--
-- Table structure for table `ideas_comment`
--

CREATE TABLE `ideas_comment` (
  `id` bigint(20) NOT NULL,
  `text` longtext NOT NULL,
  `idea_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ideas_conversation`
--

CREATE TABLE `ideas_conversation` (
  `id` bigint(20) NOT NULL,
  `subject` varchar(255) NOT NULL DEFAULT '(No Subject)',
  `user1_id` bigint(20) NOT NULL,
  `user2_id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ideas_customuser`
--

CREATE TABLE `ideas_customuser` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `dob` date DEFAULT NULL,
  `is_student` tinyint(1) NOT NULL,
  `school_name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ideas_customuser`
--

INSERT INTO `ideas_customuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `email`, `dob`, `is_student`, `school_name`, `phone_number`) VALUES
(2, 'pbkdf2_sha256$600000$dXoeAk0g3Eyvz8ysSlrrSF$a6zQ+BsH61pasB8CTvI+yj1762HXW+bIfXcbEVbxu8I=', '2025-09-09 02:40:59.680191', 0, 'FI.programming.tamil@gmail.com', 'Ashwanth', 'S', 0, 1, '2025-09-04 20:11:37.285574', 'ashwanth.ars@gmail.com', '2012-02-12', 0, NULL, '09894843555'),
(4, 'pbkdf2_sha256$600000$90tZHQJmi6UGB7AemJqwRD$Xf+cyd0TSAZxdmVN718tl8nF33kyY/S9GTF/RFTyqJE=', '2025-09-09 03:02:30.465349', 0, 'savi', 'Savitha', 'K', 0, 1, '2025-09-09 02:39:32.168950', 'savi@gmail.com', '2010-04-28', 1, 'AVP Public Senior secondary school', '1234567890'),
(5, 'pbkdf2_sha256$600000$whzD1uXzjDRqRZG7RGTwId$iqlGqhIlMil9Vu8cGPTAp4KdhaHnesky5iYYYgQhdqI=', '2025-09-09 03:03:35.362892', 0, 'gukesh', 'Gukesh', 'SJ', 0, 1, '2025-09-09 02:55:32.918999', 'gukesh@gmail.com', '2005-01-10', 1, 'Nachammal', '1234567890');

-- --------------------------------------------------------

--
-- Table structure for table `ideas_customuser_groups`
--

CREATE TABLE `ideas_customuser_groups` (
  `id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ideas_customuser_user_permissions`
--

CREATE TABLE `ideas_customuser_user_permissions` (
  `id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ideas_follow`
--

CREATE TABLE `ideas_follow` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `follower_id` bigint(20) NOT NULL,
  `following_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ideas_follow`
--

INSERT INTO `ideas_follow` (`id`, `created_at`, `follower_id`, `following_id`) VALUES
(6, '2025-09-09 02:42:35.053779', 2, 4),
(7, '2025-09-09 02:44:43.398014', 4, 2),
(8, '2025-09-09 02:55:48.437528', 5, 4),
(9, '2025-09-09 02:55:56.036714', 5, 2),
(10, '2025-09-09 03:02:51.420428', 4, 5);

-- --------------------------------------------------------

--
-- Table structure for table `ideas_forumpost`
--

CREATE TABLE `ideas_forumpost` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `category` varchar(20) NOT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `document` varchar(100) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `slug` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ideas_forumpost`
--

INSERT INTO `ideas_forumpost` (`id`, `title`, `content`, `category`, `created_by_id`, `document`, `image`, `created_at`, `slug`) VALUES
(2, 'Hello', 'Hello world', 'tech', 2, '', '', '2025-09-08 18:57:44.906018', NULL),
(3, 'Help Required to create Idea', 'Hello Members,\r\nPlease help me create new ideas.', 'other', 4, '', '', '2025-09-09 02:53:18.610126', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `ideas_forumpostcomment`
--

CREATE TABLE `ideas_forumpostcomment` (
  `id` bigint(20) NOT NULL,
  `text` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_accepted` tinyint(1) NOT NULL,
  `forum_post_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ideas_forumpostlike`
--

CREATE TABLE `ideas_forumpostlike` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `forum_post_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ideas_forumpostreport`
--

CREATE TABLE `ideas_forumpostreport` (
  `id` bigint(20) NOT NULL,
  `reason` longtext NOT NULL,
  `reported_at` datetime(6) NOT NULL,
  `forum_post_id` bigint(20) NOT NULL,
  `reported_by_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ideas_idea`
--

CREATE TABLE `ideas_idea` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `description` longtext NOT NULL,
  `category` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint(20) NOT NULL,
  `is_archived` tinyint(1) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `document` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ideas_idea`
--

INSERT INTO `ideas_idea` (`id`, `title`, `slug`, `description`, `category`, `created_at`, `created_by_id`, `is_archived`, `image`, `document`) VALUES
(3, 'Fitbro', 'fit4fun-home-fitness', 'Fit4Fun: Home Fitness Challenge is your ultimate companion for staying active, energized, and motivated—all from the comfort of your home. Designed for individuals of all fitness levels, this challenge blends fun, flexibility, and results into a dynamic daily routine that fits your lifestyle. Whether you\'re a beginner looking to kickstart your wellness journey or a seasoned fitness enthusiast seeking variety, Fit4Fun offers a structured yet adaptable program that keeps you moving and smiling.\r\nEach day introduces a new workout theme—from cardio bursts and core sculpting to balance training and flexibility flows. No fancy equipment needed—just your body, a bit of space, and a commitment to show up. With short, effective sessions ranging from 10 to 20 minutes, Fit4Fun makes it easy to squeeze in fitness between meetings, chores, or study breaks.\r\nThe challenge also includes a progress tracker to log your workouts, celebrate milestones, and stay accountable. You’ll find motivational tips, curated video links, and', 'sports', '2025-09-04 20:13:58.105303', 2, 0, NULL, NULL),
(4, 'GreenLoop', 'greenloop', 'GreenLoop is a digital platform that connects individuals and businesses to local recycling, upcycling, and sustainable product services. The app uses geolocation and AI to recommend nearby drop-off points for recyclables, match users with artisans who upcycle materials into new products, and offer eco-friendly alternatives to common household items.\r\nKey features include:\r\n- ♻️ Smart Sorting Assistant: Users scan items to learn how and where to dispose of them properly\r\n- 🛍️ Eco Marketplace: A curated space for upcycled goods and sustainable brands\r\n- 📊 Impact Tracker: Visualizes users\' environmental contributions over time\r\nGreenLoop aims to make sustainability not just accessible, but rewarding—turning everyday waste into community-driven value.', 'social', '2025-09-05 08:21:56.854145', 2, 0, 'idea_images/pic_DHPviVX.webp', ''),
(5, 'EchoMentor', 'echomentor', 'EchoMentor is a voice-based micro-learning app that delivers daily 5-minute lessons from top experts in fields like business, psychology, and design. Users choose a topic, and the app sends bite-sized audio insights each morning—perfect for commutes or coffee breaks. It also includes interactive voice quizzes to reinforce learning and track progress over time. EchoMentor turns passive listening into active growth, making expert knowledge accessible and engaging for busy minds.', 'tech', '2025-09-05 08:22:30.263614', 2, 0, NULL, NULL),
(6, 'MindMesh', 'mindmesh', 'MindMesh is a collaborative brainstorming platform for remote teams, designed to mimic the energy of in-person ideation. It uses AI to suggest connections between ideas, highlight gaps, and even generate creative prompts based on team goals. With real-time sketching, voice notes, and mood boards, MindMesh helps teams co-create like they\'re in the same room—even when they\'re continents apart. It’s like a digital whiteboard with a brain of its own.', 'tech', '2025-09-05 08:22:52.729942', 2, 0, 'idea_images/pic_CKvw4hP.jpeg', ''),
(8, 'MoneyMinds: Smart Finance for Super Kids', 'moneyminds-smart-finance-for-super-kids', '🎯 Concept Overview\r\nMoneyMinds is a kid-friendly financial education and planning service that helps children understand money, build saving habits, and prepare for future financial independence. It’s split into two age-based tracks:\r\n\r\nMini MoneyMinds (Ages 5–12): Focus on saving at home, understanding needs vs. wants, and playful budgeting\r\nMajor MoneyMinds (Ages 13–19): Learn banking basics, open accounts, track spending, and explore entrepreneurship.\r\n\r\n🧠 Program Structure\r\n🟡 Mini MoneyMinds (Minor Kids)\r\n      Piggy Bank Challenges: Weekly savings goals with fun themes (e.g., “Save for a Space Toy!”)\r\n      Money Storytime: Short tales about earning, spending, and sharing\r\nDIY Budget Boards: Kids create visual boards to plan how they’ll use their allowance\r\n     Role-Play Shops: Simulate buying/selling with play money to teach value and decision-making\r\n     Savings Tracker Sheets: Colorful charts to track progress and celebrate milestones\r\n\r\n🔵 Major MoneyMinds (Teen Kids)\r\n     Banking 101: Guide to opening savings accounts, understanding interest, and using debit cards\r\n     Budget Bootcamp: Teach monthly planning, expense tracking, and goal setting\r\nSmart Spending Tips: How to avoid impulse buys and compare value\r\nMini Biz Builders: Encourage small business ideas with budgeting and profit tracking\r\n    Digital Tools: Introduce apps or spreadsheets for managing money safely.', 'business', '2025-09-09 02:49:24.956868', 4, 0, '', ''),
(9, 'Trash to Art Club', 'trash-to-art-club', '🌟 Mission\r\nTo inspire kids to see beauty in discarded materials, reduce waste, and express themselves through eco-conscious art.\r\n\r\n🛠️ How It Works\r\n1. Collection & Sorting\r\nStudents bring clean recyclables: boxes, bottles, caps, wrappers, cardboard\r\nSet up sorting stations labeled “Buildables,” “Decoratives,” “Mystery Materials”\r\nEncourage themed collections: “Space Junk,” “Jungle Bits,” “Robot Parts”\r\n\r\n2. Creative Workshops\r\nWeekly or monthly sessions with guided themes:\r\nBottle Buddies: Make characters from plastic bottles\r\nBox City: Build a miniature town from cartons\r\nEco-Masks: Create wearable art from mixed materials\r\nInvite local artists or teachers to lead special sessions\r\n\r\n3. Showcase & Celebrate\r\nHost “Trash to Treasure” exhibitions at school\r\nCreate an online gallery or social media page for student creations\r\nGive awards like “Most Inventive,” “Best Use of Materials,” “Eco Storyteller”', 'art', '2025-09-09 02:57:16.578342', 5, 0, '', '');

-- --------------------------------------------------------

--
-- Table structure for table `ideas_idea_starred_by`
--

CREATE TABLE `ideas_idea_starred_by` (
  `id` bigint(20) NOT NULL,
  `idea_id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ideas_idea_starred_by`
--

INSERT INTO `ideas_idea_starred_by` (`id`, `idea_id`, `customuser_id`) VALUES
(2, 3, 2),
(3, 6, 4),
(5, 8, 5);

-- --------------------------------------------------------

--
-- Table structure for table `ideas_like`
--

CREATE TABLE `ideas_like` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `idea_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ideas_like`
--

INSERT INTO `ideas_like` (`id`, `created_at`, `idea_id`, `user_id`) VALUES
(5, '2025-09-05 08:26:58.515615', 3, 2),
(6, '2025-09-09 02:40:21.336093', 6, 4),
(7, '2025-09-09 02:59:36.627646', 9, 5),
(9, '2025-09-09 03:01:08.031911', 8, 5);

-- --------------------------------------------------------

--
-- Table structure for table `ideas_message`
--

CREATE TABLE `ideas_message` (
  `id` bigint(20) NOT NULL,
  `conversation_id` bigint(20) NOT NULL,
  `sender_id` bigint(20) NOT NULL,
  `subject_override` varchar(255) NOT NULL DEFAULT '',
  `text` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL DEFAULT 0,
  `is_reported` tinyint(1) NOT NULL DEFAULT 0,
  `folder` varchar(20) NOT NULL DEFAULT 'inbox',
  `attachment` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ideas_message`
--

INSERT INTO `ideas_message` (`id`, `conversation_id`, `sender_id`, `subject_override`, `text`, `timestamp`, `is_read`, `is_reported`, `folder`, `attachment`) VALUES
(7, 2, 4, 'Hi test', 'Hi, This is test message.', '2025-09-09 02:50:25.613335', 1, 0, 'sent', ''),
(8, 2, 4, 'Hi test', 'Hi, This is test message.', '2025-09-09 02:50:25.615337', 1, 0, 'inbox', ''),
(9, 2, 2, 'Hi Savi', 'Hi Savi,\r\nThis is test message.', '2025-09-09 02:51:02.924699', 1, 0, 'sent', ''),
(10, 2, 2, 'Hi Savi', 'Hi Savi,\r\nThis is test message.', '2025-09-09 02:51:02.925699', 1, 0, 'inbox', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `conversation`
--
ALTER TABLE `conversation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ideas_conversation_user1_id_fk` (`user1_id`),
  ADD KEY `ideas_conversation_user2_id_fk` (`user2_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_ideas_customuser_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `ideas_comment`
--
ALTER TABLE `ideas_comment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ideas_comment_idea_id_0ab5ade0_fk_ideas_idea_id` (`idea_id`),
  ADD KEY `ideas_comment_user_id_fede6dcd_fk_ideas_customuser_id` (`user_id`);

--
-- Indexes for table `ideas_conversation`
--
ALTER TABLE `ideas_conversation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_convo_user1` (`user1_id`),
  ADD KEY `idx_convo_user2` (`user2_id`);

--
-- Indexes for table `ideas_customuser`
--
ALTER TABLE `ideas_customuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `ideas_customuser_groups`
--
ALTER TABLE `ideas_customuser_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ideas_customuser_groups_customuser_id_group_id_4c3f981d_uniq` (`customuser_id`,`group_id`),
  ADD KEY `ideas_customuser_groups_group_id_068fe800_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `ideas_customuser_user_permissions`
--
ALTER TABLE `ideas_customuser_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ideas_customuser_user_pe_customuser_id_permission_7e388729_uniq` (`customuser_id`,`permission_id`),
  ADD KEY `ideas_customuser_use_permission_id_7b1bec4e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `ideas_follow`
--
ALTER TABLE `ideas_follow`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ideas_follow_follower_id_following_id_2d96f93a_uniq` (`follower_id`,`following_id`),
  ADD KEY `ideas_follow_following_id_0f2025be_fk_ideas_customuser_id` (`following_id`);

--
-- Indexes for table `ideas_forumpost`
--
ALTER TABLE `ideas_forumpost`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `ideas_forumpost_created_by_id_fd13e23b_fk_ideas_customuser_id` (`created_by_id`);

--
-- Indexes for table `ideas_forumpostcomment`
--
ALTER TABLE `ideas_forumpostcomment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ideas_forumpostcomme_forum_post_id_646e3ec4_fk_ideas_for` (`forum_post_id`),
  ADD KEY `ideas_forumpostcomment_user_id_43b822c1_fk_ideas_customuser_id` (`user_id`);

--
-- Indexes for table `ideas_forumpostlike`
--
ALTER TABLE `ideas_forumpostlike`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ideas_forumpostlike_forum_post_id_user_id_cf50289d_uniq` (`forum_post_id`,`user_id`),
  ADD KEY `ideas_forumpostlike_user_id_6e2ee724_fk_ideas_customuser_id` (`user_id`);

--
-- Indexes for table `ideas_forumpostreport`
--
ALTER TABLE `ideas_forumpostreport`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ideas_forumpostrepor_forum_post_id_0b057873_fk_ideas_for` (`forum_post_id`),
  ADD KEY `ideas_forumpostrepor_reported_by_id_abc86b53_fk_ideas_cus` (`reported_by_id`);

--
-- Indexes for table `ideas_idea`
--
ALTER TABLE `ideas_idea`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `ideas_idea_created_by_id_0fc510ae_fk_ideas_customuser_id` (`created_by_id`);

--
-- Indexes for table `ideas_idea_starred_by`
--
ALTER TABLE `ideas_idea_starred_by`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ideas_idea_starred_by_idea_id_customuser_id_5dc766cc_uniq` (`idea_id`,`customuser_id`),
  ADD KEY `ideas_idea_starred_b_customuser_id_c33aa23d_fk_ideas_cus` (`customuser_id`);

--
-- Indexes for table `ideas_like`
--
ALTER TABLE `ideas_like`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ideas_like_idea_id_user_id_9438bed7_uniq` (`idea_id`,`user_id`),
  ADD KEY `ideas_like_user_id_c06e7c17_fk_ideas_customuser_id` (`user_id`);

--
-- Indexes for table `ideas_message`
--
ALTER TABLE `ideas_message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ideas_message_conversation_id_fk` (`conversation_id`),
  ADD KEY `ideas_message_sender_id_fk` (`sender_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT for table `conversation`
--
ALTER TABLE `conversation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `ideas_comment`
--
ALTER TABLE `ideas_comment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `ideas_conversation`
--
ALTER TABLE `ideas_conversation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ideas_customuser`
--
ALTER TABLE `ideas_customuser`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `ideas_customuser_groups`
--
ALTER TABLE `ideas_customuser_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ideas_customuser_user_permissions`
--
ALTER TABLE `ideas_customuser_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ideas_follow`
--
ALTER TABLE `ideas_follow`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `ideas_forumpost`
--
ALTER TABLE `ideas_forumpost`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `ideas_forumpostcomment`
--
ALTER TABLE `ideas_forumpostcomment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ideas_forumpostlike`
--
ALTER TABLE `ideas_forumpostlike`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `ideas_forumpostreport`
--
ALTER TABLE `ideas_forumpostreport`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ideas_idea`
--
ALTER TABLE `ideas_idea`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `ideas_idea_starred_by`
--
ALTER TABLE `ideas_idea_starred_by`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `ideas_like`
--
ALTER TABLE `ideas_like`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `ideas_message`
--
ALTER TABLE `ideas_message`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `conversation`
--
ALTER TABLE `conversation`
  ADD CONSTRAINT `ideas_conversation_user1_id_fk` FOREIGN KEY (`user1_id`) REFERENCES `ideas_customuser` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ideas_conversation_user2_id_fk` FOREIGN KEY (`user2_id`) REFERENCES `ideas_customuser` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_ideas_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `ideas_customuser` (`id`);

--
-- Constraints for table `ideas_comment`
--
ALTER TABLE `ideas_comment`
  ADD CONSTRAINT `ideas_comment_idea_id_0ab5ade0_fk_ideas_idea_id` FOREIGN KEY (`idea_id`) REFERENCES `ideas_idea` (`id`),
  ADD CONSTRAINT `ideas_comment_user_id_fede6dcd_fk_ideas_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `ideas_customuser` (`id`);

--
-- Constraints for table `ideas_conversation`
--
ALTER TABLE `ideas_conversation`
  ADD CONSTRAINT `fk_convo_user1` FOREIGN KEY (`user1_id`) REFERENCES `ideas_customuser` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_convo_user2` FOREIGN KEY (`user2_id`) REFERENCES `ideas_customuser` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `ideas_customuser_groups`
--
ALTER TABLE `ideas_customuser_groups`
  ADD CONSTRAINT `ideas_customuser_gro_customuser_id_8a1bd3ca_fk_ideas_cus` FOREIGN KEY (`customuser_id`) REFERENCES `ideas_customuser` (`id`),
  ADD CONSTRAINT `ideas_customuser_groups_group_id_068fe800_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `ideas_customuser_user_permissions`
--
ALTER TABLE `ideas_customuser_user_permissions`
  ADD CONSTRAINT `ideas_customuser_use_customuser_id_2ea7c69f_fk_ideas_cus` FOREIGN KEY (`customuser_id`) REFERENCES `ideas_customuser` (`id`),
  ADD CONSTRAINT `ideas_customuser_use_permission_id_7b1bec4e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `ideas_follow`
--
ALTER TABLE `ideas_follow`
  ADD CONSTRAINT `ideas_follow_follower_id_bb77902c_fk_ideas_customuser_id` FOREIGN KEY (`follower_id`) REFERENCES `ideas_customuser` (`id`),
  ADD CONSTRAINT `ideas_follow_following_id_0f2025be_fk_ideas_customuser_id` FOREIGN KEY (`following_id`) REFERENCES `ideas_customuser` (`id`);

--
-- Constraints for table `ideas_forumpost`
--
ALTER TABLE `ideas_forumpost`
  ADD CONSTRAINT `ideas_forumpost_created_by_id_fd13e23b_fk_ideas_customuser_id` FOREIGN KEY (`created_by_id`) REFERENCES `ideas_customuser` (`id`);

--
-- Constraints for table `ideas_forumpostcomment`
--
ALTER TABLE `ideas_forumpostcomment`
  ADD CONSTRAINT `ideas_forumpostcomme_forum_post_id_646e3ec4_fk_ideas_for` FOREIGN KEY (`forum_post_id`) REFERENCES `ideas_forumpost` (`id`),
  ADD CONSTRAINT `ideas_forumpostcomment_user_id_43b822c1_fk_ideas_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `ideas_customuser` (`id`);

--
-- Constraints for table `ideas_forumpostlike`
--
ALTER TABLE `ideas_forumpostlike`
  ADD CONSTRAINT `ideas_forumpostlike_forum_post_id_fbdcfcaf_fk_ideas_forumpost_id` FOREIGN KEY (`forum_post_id`) REFERENCES `ideas_forumpost` (`id`),
  ADD CONSTRAINT `ideas_forumpostlike_user_id_6e2ee724_fk_ideas_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `ideas_customuser` (`id`);

--
-- Constraints for table `ideas_forumpostreport`
--
ALTER TABLE `ideas_forumpostreport`
  ADD CONSTRAINT `ideas_forumpostrepor_forum_post_id_0b057873_fk_ideas_for` FOREIGN KEY (`forum_post_id`) REFERENCES `ideas_forumpost` (`id`),
  ADD CONSTRAINT `ideas_forumpostrepor_reported_by_id_abc86b53_fk_ideas_cus` FOREIGN KEY (`reported_by_id`) REFERENCES `ideas_customuser` (`id`);

--
-- Constraints for table `ideas_idea`
--
ALTER TABLE `ideas_idea`
  ADD CONSTRAINT `ideas_idea_created_by_id_0fc510ae_fk_ideas_customuser_id` FOREIGN KEY (`created_by_id`) REFERENCES `ideas_customuser` (`id`);

--
-- Constraints for table `ideas_idea_starred_by`
--
ALTER TABLE `ideas_idea_starred_by`
  ADD CONSTRAINT `ideas_idea_starred_b_customuser_id_c33aa23d_fk_ideas_cus` FOREIGN KEY (`customuser_id`) REFERENCES `ideas_customuser` (`id`),
  ADD CONSTRAINT `ideas_idea_starred_by_idea_id_aef08b9e_fk_ideas_idea_id` FOREIGN KEY (`idea_id`) REFERENCES `ideas_idea` (`id`);

--
-- Constraints for table `ideas_like`
--
ALTER TABLE `ideas_like`
  ADD CONSTRAINT `ideas_like_idea_id_435284e5_fk_ideas_idea_id` FOREIGN KEY (`idea_id`) REFERENCES `ideas_idea` (`id`),
  ADD CONSTRAINT `ideas_like_user_id_c06e7c17_fk_ideas_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `ideas_customuser` (`id`);

--
-- Constraints for table `ideas_message`
--
ALTER TABLE `ideas_message`
  ADD CONSTRAINT `ideas_message_conversation_id_fk` FOREIGN KEY (`conversation_id`) REFERENCES `conversation` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ideas_message_sender_id_fk` FOREIGN KEY (`sender_id`) REFERENCES `ideas_customuser` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
