-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 05, 2025 at 12:56 PM
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
(40, 'Can view follow', 10, 'view_follow');

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
(6, 'ideas', 'customuser'),
(10, 'ideas', 'follow'),
(7, 'ideas', 'idea'),
(9, 'ideas', 'like'),
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
(21, 'ideas', '0003_idea_is_archived', '2025-09-04 21:05:06.817556');

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
('fwo3g98ioodwebg5xxs7h9n9jyippl5b', '.eJxVjDkOwjAURO_iGll4kw0lPWew_mYcQI4UJ1XE3UmkFFDOvDezqgzLXPPSZcoDq6uy6vTbIdBL2g74Ce0xahrbPA2od0UftOv7yPK-He7fQYVet_U5IiTgSCGIj4SXYiRggOQwWBtdIhbyYgx4b5wtBYHdli1EoWST-nwB_kc4hQ:1uuS99:zvHUTkuZ6wzzJQKTjCYaxyhEpDAaQUou20PIKFXPh5o', '2025-09-19 08:50:15.508935');

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
(2, 'pbkdf2_sha256$600000$dXoeAk0g3Eyvz8ysSlrrSF$a6zQ+BsH61pasB8CTvI+yj1762HXW+bIfXcbEVbxu8I=', '2025-09-05 08:50:15.507929', 0, 'FI.programming.tamil@gmail.com', 'Ashwanth', 'S', 0, 1, '2025-09-04 20:11:37.285574', 'ashwanth.ars@gmail.com', '2012-02-12', 0, '', '09894843555');

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
  `is_archived` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ideas_idea`
--

INSERT INTO `ideas_idea` (`id`, `title`, `slug`, `description`, `category`, `created_at`, `created_by_id`, `is_archived`) VALUES
(3, 'Fitbro', 'fit4fun-home-fitness', 'Fit4Fun: Home Fitness Challenge is your ultimate companion for staying active, energized, and motivated—all from the comfort of your home. Designed for individuals of all fitness levels, this challenge blends fun, flexibility, and results into a dynamic daily routine that fits your lifestyle. Whether you\'re a beginner looking to kickstart your wellness journey or a seasoned fitness enthusiast seeking variety, Fit4Fun offers a structured yet adaptable program that keeps you moving and smiling.\r\nEach day introduces a new workout theme—from cardio bursts and core sculpting to balance training and flexibility flows. No fancy equipment needed—just your body, a bit of space, and a commitment to show up. With short, effective sessions ranging from 10 to 20 minutes, Fit4Fun makes it easy to squeeze in fitness between meetings, chores, or study breaks.\r\nThe challenge also includes a progress tracker to log your workouts, celebrate milestones, and stay accountable. You’ll find motivational tips, curated video links, and', 'sports', '2025-09-04 20:13:58.105303', 2, 0),
(4, 'GreenLoop', 'greenloop', 'GreenLoop is a digital platform that connects individuals and businesses to local recycling, upcycling, and sustainable product services. The app uses geolocation and AI to recommend nearby drop-off points for recyclables, match users with artisans who upcycle materials into new products, and offer eco-friendly alternatives to common household items.\r\nKey features include:\r\n- ♻️ Smart Sorting Assistant: Users scan items to learn how and where to dispose of them properly\r\n- 🛍️ Eco Marketplace: A curated space for upcycled goods and sustainable brands\r\n- 📊 Impact Tracker: Visualizes users\' environmental contributions over time\r\nGreenLoop aims to make sustainability not just accessible, but rewarding—turning everyday waste into community-driven value.', 'social', '2025-09-05 08:21:56.854145', 2, 0),
(5, 'EchoMentor', 'echomentor', 'EchoMentor is a voice-based micro-learning app that delivers daily 5-minute lessons from top experts in fields like business, psychology, and design. Users choose a topic, and the app sends bite-sized audio insights each morning—perfect for commutes or coffee breaks. It also includes interactive voice quizzes to reinforce learning and track progress over time. EchoMentor turns passive listening into active growth, making expert knowledge accessible and engaging for busy minds.', 'tech', '2025-09-05 08:22:30.263614', 2, 0),
(6, 'MindMesh', 'mindmesh', 'MindMesh is a collaborative brainstorming platform for remote teams, designed to mimic the energy of in-person ideation. It uses AI to suggest connections between ideas, highlight gaps, and even generate creative prompts based on team goals. With real-time sketching, voice notes, and mood boards, MindMesh helps teams co-create like they\'re in the same room—even when they\'re continents apart. It’s like a digital whiteboard with a brain of its own.', 'tech', '2025-09-05 08:22:52.729942', 2, 0);

-- --------------------------------------------------------

--
-- Table structure for table `ideas_idea_starred_by`
--

CREATE TABLE `ideas_idea_starred_by` (
  `id` bigint(20) NOT NULL,
  `idea_id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(5, '2025-09-05 08:26:58.515615', 3, 2);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `ideas_comment`
--
ALTER TABLE `ideas_comment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `ideas_customuser`
--
ALTER TABLE `ideas_customuser`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

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
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `ideas_idea`
--
ALTER TABLE `ideas_idea`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `ideas_idea_starred_by`
--
ALTER TABLE `ideas_idea_starred_by`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `ideas_like`
--
ALTER TABLE `ideas_like`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

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
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
