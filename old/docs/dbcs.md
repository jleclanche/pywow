# Achievement_Category.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_parent `int`
- m_name_lang `string`
- m_ui_order `int`


# Achievement.dbc

0xf fields, 0x3c bytes

- m_ID `int`
- m_faction `int`
- m_instance_id `int`
- m_supercedes `int`
- m_title_lang `string`
- m_description_lang `string`
- m_category `int`
- m_points `int`
- m_ui_order `int`
- m_flags `int`
- m_iconID `int`
- m_reward_lang `string`
- m_minimum_criteria `int`
- m_shares_criteria `int`
- m_criteria_tree `int`


# AnimKitBoneSetAlias.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_boneDataID `int`
- m_animKitBoneSetID `int`


# AnimKitBoneSet.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_name `string`
- m_boneDataID `int`
- m_parentAnimKitBoneSetID `int`
- m_extraBoneCount `int`
- m_altAnimKitBoneSetID `int`


# AnimKitConfigBoneSet.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_parentAnimKitConfigID `int`
- m_animKitBoneSetID `int`
- m_animKitPriorityID `int`


# AnimKitConfig.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_configFlags `int`


# AnimKitPriority.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_priority `int`


# AnimKit.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_oneShotDuration `int`
- m_oneShotStopAnimKitID `int`
- m_lowDefAnimKitID `int`


# AnimKitSegment.dbc

0x11 fields, 0x44 bytes

- m_ID `int`
- m_parentAnimKitID `int`
- m_orderIndex `int`
- m_animID `int`
- m_animStartTime `int`
- m_animKitConfigID `int`
- m_startCondition `int`
- m_startConditionParam `int`
- m_startConditionDelay `int`
- m_endCondition `int`
- m_endConditionParam `int`
- m_endConditionDelay `int`
- m_speed `float`
- m_segmentFlags `int`
- m_forcedVariation `int`
- m_overrideConfigFlags `int`
- m_loopToSegmentIndex `int`


# AnimReplacement.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_srcAnimID `int`
- m_dstAnimID `int`
- m_parentAnimReplacementSetID `int`


# AnimReplacementSet.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_execOrder `int`


# AreaAssignment.dbc

0x4 fields, 0x14 bytes

- m_MapID `int`
- m_AreaID `int`
- m_ChunkX `int`
- m_ChunkY `int`


# AreaGroup.dbc

0x3 fields, 0x20 bytes

- m_ID `int`
- m_areaID_0 `int`
- m_areaID_1 `int`
- m_areaID_2 `int`
- m_areaID_3 `int`
- m_areaID_4 `int`
- m_areaID_5 `int`
- m_nextAreaID `int`


# AreaPOI.dbc

0xe fields, 0x5c bytes

- m_ID `int`
- m_importance `int`
- m_icon_0 `int`
- m_icon_1 `int`
- m_icon_2 `int`
- m_icon_3 `int`
- m_icon_4 `int`
- m_icon_5 `int`
- m_icon_6 `int`
- m_icon_7 `int`
- m_icon_8 `int`
- m_factionID `int`
- m_pos_x `float`
- m_pos_y `float`
- m_continentID `int`
- m_flags `int`
- m_areaID `int`
- m_name_lang `string`
- m_description_lang `string`
- m_worldStateID `int`
- m_playerConditionID `int`
- m_worldMapLink `int`
- m_portLocID `int`


# AreaTriggerActionSet.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_flags `int`


# AreaTriggerBox.dbc

0x2 fields, 0x10 bytes

- m_ID `int`
- m_extents_x `float`
- m_extents_y `float`
- m_extents_z `float`


# AreaTriggerCylinder.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_radius `float`
- m_height `float`


# AreaTrigger.dbc

0xf fields, 0x44 bytes

- m_ID `int`
- m_ContinentID `int`
- m_pos_x `float`
- m_pos_y `float`
- m_pos_z `float`
- m_phaseUseFlags `int`
- m_phaseID `int`
- m_phaseGroupID `int`
- m_radius `float`
- m_box_length `float`
- m_box_width `float`
- m_box_height `float`
- m_box_yaw `float`
- m_shapeType `int`
- m_shapeID `int`
- m_areaTriggerActionSetID `int`
- m_flags `int`


# AreaTriggerSphere.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_maxRadius `float`


# ArmorLocation.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_clothmodifier `float`
- m_leathermodifier `float`
- m_chainmodifier `float`
- m_platemodifier `float`
- m_modifier `float`


# AuctionHouse.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_factionID `int`
- m_depositRate `int`
- m_consignmentRate `int`
- m_name_lang `string`


# BankBagSlotPrices.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_Cost `int`


# BannedAddOns.dbc

0x5 fields, 0x2c bytes

- m_ID `int`
- m_nameMD5__0 `int`
- m_nameMD5__1 `int`
- m_nameMD5__2 `int`
- m_nameMD5__3 `int`
- m_versionMD5__0 `int`
- m_versionMD5__1 `int`
- m_versionMD5__2 `int`
- m_versionMD5__3 `int`
- m_lastModified `int`
- m_flags `int`


# BarberShopStyle.dbc

0x8 fields, 0x20 bytes

- m_ID `int`
- m_type `int`
- m_DisplayName_lang `string`
- m_Description_lang `string`
- m_Cost_Modifier `float`
- m_race `int`
- m_sex `int`
- m_data `int`


# BattlemasterList.dbc

0xf fields, 0x78 bytes

- m_ID `int`
- m_mapID_0 `int`
- m_mapID_1 `int`
- m_mapID_2 `int`
- m_mapID_3 `int`
- m_mapID_4 `int`
- m_mapID_5 `int`
- m_mapID_6 `int`
- m_mapID_7 `int`
- m_mapID_8 `int`
- m_mapID_9 `int`
- m_mapID_10 `int`
- m_mapID_11 `int`
- m_mapID_12 `int`
- m_mapID_13 `int`
- m_mapID_14 `int`
- m_mapID_15 `int`
- m_instanceType `int`
- m_groupsAllowed `int`
- m_name_lang `string`
- m_maxGroupSize `int`
- m_holidayWorldState `int`
- m_minlevel `int`
- m_maxlevel `int`
- m_ratedPlayers `int`
- m_minPlayers `int`
- m_maxPlayers `int`
- m_flags `int`
- m_iconFileDataID `int`
- m_gametype_lang `string`


# CameraMode.dbc

0xd fields, 0x44 bytes

- m_ID `int`
- m_name `string`
- m_type `int`
- m_flags `int`
- m_positionOffset_x `float`
- m_positionOffset_y `float`
- m_positionOffset_z `float`
- m_targetOffset_x `float`
- m_targetOffset_y `float`
- m_targetOffset_z `float`
- m_positionSmoothing `float`
- m_rotationSmoothing `float`
- m_fieldOfView `float`
- m_lockedPositionOffsetBase `int`
- m_lockedPositionOffsetDirection `int`
- m_lockedTargetOffsetBase `int`
- m_lockedTargetOffsetDirection `int`


# CameraShakes.dbc

0x9 fields, 0x24 bytes

- m_ID `int`
- m_shakeType `int`
- m_direction `int`
- m_amplitude `float`
- m_frequency `float`
- m_duration `float`
- m_phase `float`
- m_coefficient `float`
- m_flags `int`


# CastableRaidBuffs.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_spellID `int`
- m_castingSpellID `int`


# Cfg_Categories.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_localeMask `int`
- m_create_charsetMask `int`
- m_existing_charsetMask `int`
- m_flags `int`
- m_name_lang `string`


# Cfg_Configs.dbc

0x6 fields, 0x1c bytes

- m_ID `int`
- m_realmType `int`
- m_playerKillingAllowed `int`
- m_roleplaying `int`
- m_playerAttackSpeedBase `int`
- m_maxDamageReductionPctPhysical `int`


# Cfg_Regions.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_tag `string`
- m_region_group_mask `int`
- m_rulesetID `int`


# CharacterFacialHairStyles.dbc

0x4 fields, 0x24 bytes

- m_raceID `int`
- m_sexID `int`
- m_VariationID `int`
- m_Geoset_0 `int`
- m_Geoset_1 `int`
- m_Geoset_2 `int`
- m_Geoset_3 `int`
- m_Geoset_4 `int`


# CharacterLoadoutItem.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_characterLoadoutID `int`
- m_itemID `int`
- m_itemDisplayInfoID `int`
- m_itemInventoryType `int`


# CharacterLoadout.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_chrClassID `int`
- m_purpose `int`
- m_racemask `int`


# CharBaseInfo.dbc

0x2 fields, 0x8 bytes

- m_raceID `int`
- m_classID `int`


# CharBaseSection.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_fallbackID `int`
- m_layoutResType `int`


# CharComponentTextureLayouts.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_width `int`
- m_height `int`


# CharComponentTextureSections.dbc

0x7 fields, 0x1c bytes

- m_ID `int`
- m_charComponentTextureLayoutID `int`
- m_sectionType `int`
- m_x `int`
- m_y `int`
- m_width `int`
- m_height `int`


# CharHairGeosets.dbc

0x9 fields, 0x24 bytes

- m_ID `int`
- m_RaceID `int`
- m_SexID `int`
- m_VariationID `int`
- m_VariationType `int`
- m_GeosetID `int`
- m_GeosetType `int`
- m_Showscalp `int`
- m_ColorIndex `int`


# CharSections.dbc

0x8 fields, 0x28 bytes

- m_ID `int`
- m_raceID `int`
- m_sexID `int`
- m_baseSection `int`
- m_TextureName_0 `string`
- m_TextureName_1 `string`
- m_TextureName_2 `string`
- m_flags `int`
- m_variationIndex `int`
- m_colorIndex `int`


# CharStartOutfit.dbc

0xa fields, 0x130 bytes

- m_ID `int`
- m_raceID `int`
- m_classID `int`
- m_sexID `int`
- m_outfitID `int`
- m_ItemID_0 `int`
- m_ItemID_1 `int`
- m_ItemID_2 `int`
- m_ItemID_3 `int`
- m_ItemID_4 `int`
- m_ItemID_5 `int`
- m_ItemID_6 `int`
- m_ItemID_7 `int`
- m_ItemID_8 `int`
- m_ItemID_9 `int`
- m_ItemID_10 `int`
- m_ItemID_11 `int`
- m_ItemID_12 `int`
- m_ItemID_13 `int`
- m_ItemID_14 `int`
- m_ItemID_15 `int`
- m_ItemID_16 `int`
- m_ItemID_17 `int`
- m_ItemID_18 `int`
- m_ItemID_19 `int`
- m_ItemID_20 `int`
- m_ItemID_21 `int`
- m_ItemID_22 `int`
- m_ItemID_23 `int`
- m_DisplayItemID_0 `int`
- m_DisplayItemID_1 `int`
- m_DisplayItemID_2 `int`
- m_DisplayItemID_3 `int`
- m_DisplayItemID_4 `int`
- m_DisplayItemID_5 `int`
- m_DisplayItemID_6 `int`
- m_DisplayItemID_7 `int`
- m_DisplayItemID_8 `int`
- m_DisplayItemID_9 `int`
- m_DisplayItemID_10 `int`
- m_DisplayItemID_11 `int`
- m_DisplayItemID_12 `int`
- m_DisplayItemID_13 `int`
- m_DisplayItemID_14 `int`
- m_DisplayItemID_15 `int`
- m_DisplayItemID_16 `int`
- m_DisplayItemID_17 `int`
- m_DisplayItemID_18 `int`
- m_DisplayItemID_19 `int`
- m_DisplayItemID_20 `int`
- m_DisplayItemID_21 `int`
- m_DisplayItemID_22 `int`
- m_DisplayItemID_23 `int`
- m_InventoryType_0 `int`
- m_InventoryType_1 `int`
- m_InventoryType_2 `int`
- m_InventoryType_3 `int`
- m_InventoryType_4 `int`
- m_InventoryType_5 `int`
- m_InventoryType_6 `int`
- m_InventoryType_7 `int`
- m_InventoryType_8 `int`
- m_InventoryType_9 `int`
- m_InventoryType_10 `int`
- m_InventoryType_11 `int`
- m_InventoryType_12 `int`
- m_InventoryType_13 `int`
- m_InventoryType_14 `int`
- m_InventoryType_15 `int`
- m_InventoryType_16 `int`
- m_InventoryType_17 `int`
- m_InventoryType_18 `int`
- m_InventoryType_19 `int`
- m_InventoryType_20 `int`
- m_InventoryType_21 `int`
- m_InventoryType_22 `int`
- m_InventoryType_23 `int`
- m_petDisplayID `int`
- m_petFamilyID `int`


# CharTitles.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_Condition_ID `int`
- m_name_lang `string`
- m_name1_lang `string`
- m_mask_ID `int`
- m_flags `int`


# ChatChannels.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_flags `int`
- m_factionGroup `int`
- m_name_lang `string`
- m_shortcut_lang `string`


# ChatProfanity.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_text `string`
- m_Language `int`


# ChrClasses.dbc

0x12 fields, 0x48 bytes

- m_ID `int`
- m_DisplayPower `int`
- m_petNameToken `string`
- m_name_lang `string`
- m_name_female_lang `string`
- m_name_male_lang `string`
- m_filename `string`
- m_spellClassSet `int`
- m_flags `int`
- m_cinematicSequenceID `int`
- m_attackPowerPerStrength `int`
- m_attackPowerPerAgility `int`
- m_rangedAttackPowerPerAgility `int`
- m_defaultSpec `int`
- m_createScreenFileDataID `int`
- m_selectScreenFileDataID `int`
- m_lowResScreenFileDataID `int`
- m_iconFileDataID `int`


# ChrClassesXPowerTypes.dbc

0x2 fields, 0xc bytes

- m_classID `int`
- m_powerType `int`


# ChrRaces.dbc

0x22 fields, 0x9c bytes

- m_ID `int`
- m_flags `int`
- m_factionID `int`
- m_ExplorationSoundID `int`
- m_MaleDisplayId `int`
- m_FemaleDisplayId `int`
- m_ClientPrefix `string`
- m_BaseLanguage `int`
- m_creatureType `int`
- m_ResSicknessSpellID `int`
- m_SplashSoundID `int`
- m_clientFileString `string`
- m_cinematicSequenceID `int`
- m_alliance `int`
- m_name_lang `string`
- m_name_female_lang `string`
- m_name_male_lang `string`
- m_facialHairCustomization_0 `string`
- m_facialHairCustomization_1 `string`
- m_hairCustomization `string`
- m_race_related `int`
- m_unalteredVisualRaceID `int`
- m_uaMaleCreatureSoundDataID `int`
- m_uaFemaleCreatureSoundDataID `int`
- m_charComponentTextureLayoutID `int`
- m_defaultClassID `int`
- m_createScreenFileDataID `int`
- m_selectScreenFileDataID `int`
- m_maleCustomizeOffset_x `float`
- m_maleCustomizeOffset_y `float`
- m_maleCustomizeOffset_z `float`
- m_femaleCustomizeOffset_x `float`
- m_femaleCustomizeOffset_y `float`
- m_femaleCustomizeOffset_z `float`
- m_neutralRaceID `int`
- m_lowResScreenFileDataID `int`
- m_HighResMaleDisplayId `int`
- m_HighResFemaleDisplayId `int`
- m_charComponentTexLayoutHiResID `int`


# ChrSpecialization.dbc

0xe fields, 0x44 bytes

- m_ID `int`
- m_backgroundFile `string`
- m_classID `int`
- m_masterySpellID_0 `int`
- m_masterySpellID_1 `int`
- m_orderIndex `int`
- m_petTalentType `int`
- m_role `int`
- m_spellIconID `int`
- m_raidBuffs `int`
- m_flags `int`
- m_name_lang `string`
- m_description_lang `string`
- m_maxBuffs `int`
- m_primaryStatOrder_0 `int`
- m_primaryStatOrder_1 `int`
- m_primaryStatOrder_2 `int`


# CinematicCamera.dbc

0x5 fields, 0x1c bytes

- m_ID `int`
- m_model `string`
- m_soundID `int`
- m_origin_x `float`
- m_origin_y `float`
- m_origin_z `float`
- m_originFacing `float`


# CinematicSequences.dbc

0x3 fields, 0x28 bytes

- m_ID `int`
- m_soundID `int`
- m_camera_0 `int`
- m_camera_1 `int`
- m_camera_2 `int`
- m_camera_3 `int`
- m_camera_4 `int`
- m_camera_5 `int`
- m_camera_6 `int`
- m_camera_7 `int`


# CombatCondition.dbc

0xc fields, 0x48 bytes

- m_ID `int`
- m_worldStateExpressionID `int`
- m_selfConditionID `int`
- m_targetConditionID `int`
- m_friendConditionID_0 `int`
- m_friendConditionID_1 `int`
- m_friendConditionOp_0 `int`
- m_friendConditionOp_1 `int`
- m_friendConditionCount_0 `int`
- m_friendConditionCount_1 `int`
- m_friendConditionLogic `int`
- m_enemyConditionID_0 `int`
- m_enemyConditionID_1 `int`
- m_enemyConditionOp_0 `int`
- m_enemyConditionOp_1 `int`
- m_enemyConditionCount_0 `int`
- m_enemyConditionCount_1 `int`
- m_enemyConditionLogic `int`


# ConsoleScripts.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_name `string`
- m_script `string`


# CreatureDisplayInfoExtra.dbc

0xc fields, 0x58 bytes

- m_ID `int`
- m_DisplayRaceID `int`
- m_DisplaySexID `int`
- m_SkinID `int`
- m_FaceID `int`
- m_HairStyleID `int`
- m_HairColorID `int`
- m_FacialHairID `int`
- m_NPCItemDisplay_0 `int`
- m_NPCItemDisplay_1 `int`
- m_NPCItemDisplay_2 `int`
- m_NPCItemDisplay_3 `int`
- m_NPCItemDisplay_4 `int`
- m_NPCItemDisplay_5 `int`
- m_NPCItemDisplay_6 `int`
- m_NPCItemDisplay_7 `int`
- m_NPCItemDisplay_8 `int`
- m_NPCItemDisplay_9 `int`
- m_NPCItemDisplay_10 `int`
- m_flags `int`
- m_fileDataID `int`
- m_hdFileDataID `int`


# CreatureDisplayInfo.dbc

0x13 fields, 0x54 bytes

- m_ID `int`
- m_modelID `int`
- m_soundID `int`
- m_extendedDisplayInfoID `int`
- m_creatureModelScale `float`
- m_creatureModelAlpha `int`
- m_textureVariation_0 `string`
- m_textureVariation_1 `string`
- m_textureVariation_2 `string`
- m_portraitTextureName `string`
- m_portraitCreatureDisplayInfoID `int`
- m_sizeClass `int`
- m_bloodID `int`
- m_NPCSoundID `int`
- m_particleColorID `int`
- m_creatureGeosetData `int`
- m_objectEffectPackageID `int`
- m_animReplacementSetID `int`
- m_flags `int`
- m_gender `int`
- m_stateSpellVisualKitID `int`


# CreatureFamily.dbc

0xb fields, 0x30 bytes

- m_ID `int`
- m_minScale `float`
- m_minScaleLevel `int`
- m_maxScale `float`
- m_maxScaleLevel `int`
- m_skillLine_0 `int`
- m_skillLine_1 `int`
- m_petFoodMask `int`
- m_petTalentType `int`
- m_categoryEnumID `int`
- m_name_lang `string`
- m_iconFile `string`


# CreatureImmunities.dbc

0xa fields, 0x78 bytes

- m_ID `int`
- m_school `int`
- m_dispelType `int`
- m_mechanicsAllowed `int`
- m_mechanic `int`
- m_effectsAllowed `int`
- m_effect_0 `int`
- m_effect_1 `int`
- m_effect_2 `int`
- m_effect_3 `int`
- m_effect_4 `int`
- m_effect_5 `int`
- m_effect_6 `int`
- m_statesAllowed `int`
- m_state_0 `int`
- m_state_1 `int`
- m_state_2 `int`
- m_state_3 `int`
- m_state_4 `int`
- m_state_5 `int`
- m_state_6 `int`
- m_state_7 `int`
- m_state_8 `int`
- m_state_9 `int`
- m_state_10 `int`
- m_state_11 `int`
- m_state_12 `int`
- m_state_13 `int`
- m_state_14 `int`
- m_flags `int`


# CreatureModelData.dbc

0x1e fields, 0x88 bytes

- m_ID `int`
- m_flags `int`
- m_fileDataID `int`
- m_sizeClass `int`
- m_modelScale `float`
- m_bloodID `int`
- m_footprintTextureID `int`
- m_footprintTextureLength `float`
- m_footprintTextureWidth `float`
- m_footprintParticleScale `float`
- m_foleyMaterialID `int`
- m_footstepShakeSize `int`
- m_deathThudShakeSize `int`
- m_soundID `int`
- m_collisionWidth `float`
- m_collisionHeight `float`
- m_mountHeight `float`
- m_geoBoxMin_x `float`
- m_geoBoxMin_y `float`
- m_geoBoxMin_z `float`
- m_geoBoxMax_x `float`
- m_geoBoxMax_y `float`
- m_geoBoxMax_z `float`
- m_worldEffectScale `float`
- m_attachedEffectScale `float`
- m_missileCollisionRadius `float`
- m_missileCollisionPush `float`
- m_missileCollisionRaise `float`
- m_overrideLootEffectScale `float`
- m_overrideNameScale `float`
- m_overrideSelectionRadius `float`
- m_tamedPetBaseScale `float`
- m_creatureGeosetDataID `int`
- m_hoverHeight `float`


# CreatureMovementInfo.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_smoothFacingChaseRate `float`


# CreatureSoundData.dbc

0x21 fields, 0xa0 bytes

- m_ID `int`
- m_soundExertionID `int`
- m_soundExertionCriticalID `int`
- m_soundInjuryID `int`
- m_soundInjuryCriticalID `int`
- m_soundInjuryCrushingBlowID `int`
- m_soundDeathID `int`
- m_soundStunID `int`
- m_soundStandID `int`
- m_soundFootstepID `int`
- m_soundAggroID `int`
- m_soundWingFlapID `int`
- m_soundWingGlideID `int`
- m_soundAlertID `int`
- m_soundFidget_0 `int`
- m_soundFidget_1 `int`
- m_soundFidget_2 `int`
- m_soundFidget_3 `int`
- m_soundFidget_4 `int`
- m_customAttack_0 `int`
- m_customAttack_1 `int`
- m_customAttack_2 `int`
- m_customAttack_3 `int`
- m_NPCSoundID `int`
- m_loopSoundID `int`
- m_creatureImpactType `int`
- m_soundJumpStartID `int`
- m_soundJumpEndID `int`
- m_soundPetAttackID `int`
- m_soundPetOrderID `int`
- m_soundPetDismissID `int`
- m_fidgetDelaySecondsMin `float`
- m_fidgetDelaySecondsMax `float`
- m_birthSoundID `int`
- m_spellCastDirectedSoundID `int`
- m_submergeSoundID `int`
- m_submergedSoundID `int`
- m_creatureSoundDataIDPet `int`
- m_transformSoundID `int`
- m_transformAnimatedSoundID `int`


# CreatureSpellData.dbc

0x3 fields, 0x24 bytes

- m_ID `int`
- m_spells_0 `int`
- m_spells_1 `int`
- m_spells_2 `int`
- m_spells_3 `int`
- m_availability_0 `int`
- m_availability_1 `int`
- m_availability_2 `int`
- m_availability_3 `int`


# CreatureType.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_name_lang `string`
- m_flags `int`


# Criteria.dbc

0xc fields, 0x30 bytes

- m_ID `int`
- m_type `int`
- m_asset `int`
- m_start_event `int`
- m_start_asset `int`
- m_start_timer `int`
- m_fail_event `int`
- m_fail_asset `int`
- m_modifier_tree_id `int`
- m_flags `int`
- m_eligibility_world_state_ID `int`
- m_eligibility_world_state_value `int`


# CriteriaTree.dbc

0x8 fields, 0x28 bytes

- m_ID `int`
- m_criteriaID `int`
- m_amount_0 `int`
- m_amount_1 `int`
- m_operator `int`
- m_parent `int`
- m_flags `int`
- m_description_lang `string`
- m_orderIndex `int`


# CriteriaTreeXEffect.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_criteriaTreeID `int`
- m_worldEffectID `int`


# CurrencyCategory.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_flags `int`
- m_name_lang `string`


# CurrencyTypes.dbc

0xb fields, 0x30 bytes

- m_ID `int`
- m_categoryID `int`
- m_name_lang `string`
- m_inventoryIcon_0 `string`
- m_inventoryIcon_1 `string`
- m_spellWeight `int`
- m_spellCategory `int`
- m_maxQty `int`
- m_maxEarnablePerWeek `int`
- m_flags `int`
- m_quality `int`
- m_description_lang `string`


# DeathThudLookups.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_SizeClass `int`
- m_TerrainTypeSoundID `int`
- m_SoundEntryID `int`
- m_SoundEntryIDWater `int`


# DeclinedWordCases.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_declinedWordID `int`
- m_caseIndex `int`
- m_declinedWord `string`


# DeclinedWord.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_word `string`


# DestructibleModelData.dbc

0x18 fields, 0x60 bytes

- m_ID `int`
- m_state0Wmo `int`
- m_state0ImpactEffectDoodadSet `int`
- m_state0AmbientDoodadSet `int`
- m_state0NameSet `int`
- m_state1Wmo `int`
- m_state1DestructionDoodadSet `int`
- m_state1ImpactEffectDoodadSet `int`
- m_state1AmbientDoodadSet `int`
- m_state1NameSet `int`
- m_state2Wmo `int`
- m_state2DestructionDoodadSet `int`
- m_state2ImpactEffectDoodadSet `int`
- m_state2AmbientDoodadSet `int`
- m_state2NameSet `int`
- m_state3Wmo `int`
- m_state3InitDoodadSet `int`
- m_state3AmbientDoodadSet `int`
- m_state3NameSet `int`
- m_ejectDirection `int`
- m_repairGroundFx `int`
- m_doNotHighlight `int`
- m_healEffect `int`
- m_healEffectSpeed `int`


# Difficulty.dbc

0xc fields, 0x30 bytes

- m_ID `int`
- m_fallbackDifficultyID `int`
- m_instanceType `int`
- m_minPlayers `int`
- m_maxPlayers `int`
- m_oldEnumValue `int`
- m_flags `int`
- m_toggleDifficultyID `int`
- m_groupSizeHealthCurveID `int`
- m_groupSizeDmgCurveID `int`
- m_groupSizeSpellPointsCurveID `int`
- m_name_lang `string`


# DungeonEncounter.dbc

0x9 fields, 0x24 bytes

- m_ID `int`
- m_mapID `int`
- m_difficultyID `int`
- m_orderIndex `int`
- m_Bit `int`
- m_name_lang `string`
- m_CreatureDisplayID `int`
- m_spellIconID `int`
- m_flags `int`


# DungeonMapChunk.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_mapID `int`
- m_wmoGroupID `int`
- m_dungeonMapID `int`
- m_minZ `float`
- m_doodadPlacementID `int`


# DungeonMap.dbc

0x7 fields, 0x24 bytes

- m_ID `int`
- m_mapID `int`
- m_floorIndex `int`
- m_min_x `float`
- m_min_y `float`
- m_max_x `float`
- m_max_y `float`
- m_parentWorldMapID `int`
- m_flags `int`


# DurabilityCosts.dbc

0x3 fields, 0x78 bytes

- m_ID `int`
- m_weaponSubClassCost_0 `int`
- m_weaponSubClassCost_1 `int`
- m_weaponSubClassCost_2 `int`
- m_weaponSubClassCost_3 `int`
- m_weaponSubClassCost_4 `int`
- m_weaponSubClassCost_5 `int`
- m_weaponSubClassCost_6 `int`
- m_weaponSubClassCost_7 `int`
- m_weaponSubClassCost_8 `int`
- m_weaponSubClassCost_9 `int`
- m_weaponSubClassCost_10 `int`
- m_weaponSubClassCost_11 `int`
- m_weaponSubClassCost_12 `int`
- m_weaponSubClassCost_13 `int`
- m_weaponSubClassCost_14 `int`
- m_weaponSubClassCost_15 `int`
- m_weaponSubClassCost_16 `int`
- m_weaponSubClassCost_17 `int`
- m_weaponSubClassCost_18 `int`
- m_weaponSubClassCost_19 `int`
- m_weaponSubClassCost_20 `int`
- m_armorSubClassCost_0 `int`
- m_armorSubClassCost_1 `int`
- m_armorSubClassCost_2 `int`
- m_armorSubClassCost_3 `int`
- m_armorSubClassCost_4 `int`
- m_armorSubClassCost_5 `int`
- m_armorSubClassCost_6 `int`
- m_armorSubClassCost_7 `int`


# DurabilityQuality.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_data `float`


# Emotes.dbc

0x8 fields, 0x20 bytes

- m_ID `int`
- m_EmoteSlashCommand `string`
- m_AnimID `int`
- m_EmoteFlags `int`
- m_EmoteSpecProc `int`
- m_EmoteSpecProcParam `int`
- m_EventSoundID `int`
- m_SpellVisualKitID `int`


# EmotesTextData.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_text_lang `string`


# EmotesText.dbc

0x4 fields, 0x4c bytes

- m_ID `int`
- m_name `string`
- m_emoteID `int`
- m_emoteText_0 `int`
- m_emoteText_1 `int`
- m_emoteText_2 `int`
- m_emoteText_3 `int`
- m_emoteText_4 `int`
- m_emoteText_5 `int`
- m_emoteText_6 `int`
- m_emoteText_7 `int`
- m_emoteText_8 `int`
- m_emoteText_9 `int`
- m_emoteText_10 `int`
- m_emoteText_11 `int`
- m_emoteText_12 `int`
- m_emoteText_13 `int`
- m_emoteText_14 `int`
- m_emoteText_15 `int`


# EmotesTextSound.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_emotesTextID `int`
- m_raceID `int`
- m_sexID `int`
- m_soundID `int`


# EnvironmentalDamage.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_EnumID `int`
- m_VisualkitID `int`


# Exhaustion.dbc

0x8 fields, 0x20 bytes

- m_ID `int`
- m_xp `int`
- m_factor `float`
- m_outdoorHours `float`
- m_innHours `float`
- m_name_lang `string`
- m_threshold `float`
- m_combatLogText `string`


# FactionGroup.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_maskID `int`
- m_internalName `string`
- m_name_lang `string`


# Faction.dbc

0xe fields, 0x70 bytes

- m_ID `int`
- m_reputationIndex `int`
- m_reputationRaceMask_0 `int`
- m_reputationRaceMask_1 `int`
- m_reputationRaceMask_2 `int`
- m_reputationRaceMask_3 `int`
- m_reputationClassMask_0 `int`
- m_reputationClassMask_1 `int`
- m_reputationClassMask_2 `int`
- m_reputationClassMask_3 `int`
- m_reputationBase_0 `int`
- m_reputationBase_1 `int`
- m_reputationBase_2 `int`
- m_reputationBase_3 `int`
- m_reputationFlags_0 `int`
- m_reputationFlags_1 `int`
- m_reputationFlags_2 `int`
- m_reputationFlags_3 `int`
- m_parentFactionID `int`
- m_parentFactionMod_x `float`
- m_parentFactionMod_y `float`
- m_parentFactionCap_0 `int`
- m_parentFactionCap_1 `int`
- m_name_lang `string`
- m_description_lang `string`
- m_expansion `int`
- m_flags `int`
- m_friendshipRepID `int`


# FactionTemplate.dbc

0x8 fields, 0x38 bytes

- m_ID `int`
- m_faction `int`
- m_flags `int`
- m_factionGroup `int`
- m_friendGroup `int`
- m_enemyGroup `int`
- m_enemies_0 `int`
- m_enemies_1 `int`
- m_enemies_2 `int`
- m_enemies_3 `int`
- m_friend_0 `int`
- m_friend_1 `int`
- m_friend_2 `int`
- m_friend_3 `int`


# FootstepTerrainLookup.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_CreatureFootstepID `int`
- m_TerrainSoundID `int`
- m_SoundID `int`
- m_SoundIDSplash `int`


# FriendshipRepReaction.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_friendshipRepID `int`
- m_reactionThreshold `int`
- m_reaction_lang `string`


# FriendshipReputation.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_factionID `int`
- m_textureFileID `int`
- m_description_lang `string`


# GameObjectArtKit.dbc

0x3 fields, 0x20 bytes

- m_ID `int`
- m_textureVariation_0 `string`
- m_textureVariation_1 `string`
- m_textureVariation_2 `string`
- m_attachModel_0 `string`
- m_attachModel_1 `string`
- m_attachModel_2 `string`
- m_attachModel_3 `string`


# GameObjectDiffAnimMap.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_gameObjectDiffAnimID `int`
- m_difficultyID `int`
- m_animation `int`
- m_attachmentDisplayID `int`


# GameObjectDisplayInfo.dbc

0x8 fields, 0x54 bytes

- m_ID `int`
- m_fileDataID `int`
- m_Sound_0 `int`
- m_Sound_1 `int`
- m_Sound_2 `int`
- m_Sound_3 `int`
- m_Sound_4 `int`
- m_Sound_5 `int`
- m_Sound_6 `int`
- m_Sound_7 `int`
- m_Sound_8 `int`
- m_Sound_9 `int`
- m_geoBoxMin_x `float`
- m_geoBoxMin_y `float`
- m_geoBoxMin_z `float`
- m_geoBoxMax_x `float`
- m_geoBoxMax_y `float`
- m_geoBoxMax_z `float`
- m_objectEffectPackageID `int`
- m_overrideLootEffectScale `float`
- m_overrideNameScale `float`


# GameTables.dbc

0x3 fields, 0x10 bytes

- m_name `string`
- m_numRows `int`
- m_numColumns `int`


# GameTips.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_text_lang `string`
- m_min_level `int`
- m_max_level `int`


# GarrUiAnimClassInfo.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_garrClassSpecID `int`
- m_spellVisualID `int`
- m_movementType `int`
- m_impactDelaySecs `float`


# GarrUiAnimRaceInfo.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_chrRaceID `int`
- m_scale `float`
- m_height `float`
- m_singleModelScale `float`
- m_singleModelHeight `float`


# GemProperties.dbc

0x6 fields, 0x18 bytes

- m_id `int`
- m_enchant_id `int`
- m_maxcount_inv `int`
- m_maxcount_item `int`
- m_type `int`
- m_min_item_level `int`


# GlueScreenEmote.dbc

0x8 fields, 0x20 bytes

- m_ID `int`
- m_classId `int`
- m_raceId `int`
- m_sexId `int`
- m_leftHandItemType `int`
- m_rightHandItemType `int`
- m_animKitId `int`
- m_spellVisualKitId `int`


# GlyphProperties.dbc

0x5 fields, 0x14 bytes

- m_id `int`
- m_spellID `int`
- m_glyphType `int`
- m_spellIconID `int`
- m_glyphExclusiveCategoryID `int`


# GlyphSlot.dbc

0x3 fields, 0xc bytes

- m_id `int`
- m_type `int`
- m_tooltip `int`


# GMSurveyAnswers.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_Sort_Index `int`
- m_GMSurveyQuestionID `int`
- m_Answer_lang `string`


# GMSurveyCurrentSurvey.dbc

0x2 fields, 0x8 bytes

- m_LANGID `int`
- m_GMSURVEY_ID `int`


# GMSurveyQuestions.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_Question_lang `string`


# GMSurveySurveys.dbc

0x2 fields, 0x40 bytes

- m_ID `int`
- m_Q_0 `int`
- m_Q_1 `int`
- m_Q_2 `int`
- m_Q_3 `int`
- m_Q_4 `int`
- m_Q_5 `int`
- m_Q_6 `int`
- m_Q_7 `int`
- m_Q_8 `int`
- m_Q_9 `int`
- m_Q_10 `int`
- m_Q_11 `int`
- m_Q_12 `int`
- m_Q_13 `int`
- m_Q_14 `int`


# GMTicketCategory.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_category_lang `string`


# GroundEffectTexture.dbc

0x5 fields, 0x2c bytes

- m_ID `int`
- m_doodadId_0 `int`
- m_doodadId_1 `int`
- m_doodadId_2 `int`
- m_doodadId_3 `int`
- m_doodadWeight_0 `int`
- m_doodadWeight_1 `int`
- m_doodadWeight_2 `int`
- m_doodadWeight_3 `int`
- m_density `int`
- m_sound `int`


# gtArmorMitigationByLvl.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtBarberShopCostBase.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtBattlePetTypeDamageMod.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtBattlePetXP.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtChanceToMeleeCritBase.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtChanceToMeleeCrit.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtChanceToSpellCritBase.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtChanceToSpellCrit.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtCombatRatings.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtItemSocketCostPerLevel.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtNPCManaCostScaler.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtOCTBaseHPByClass.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtOCTBaseMPByClass.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtOCTClassCombatRatingScalar.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_data `float`


# gtOCTHpPerStamina.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtOCTLevelExperience.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtRegenMPPerSpt.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtResilienceDR.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# gtSpellScaling.dbc

0x1 fields, 0x8 bytes

- m_data `float`


# GuildColorBackground.dbc

0x4 fields, 0x8 bytes

- m_colorID `int`
- m_red `int`
- m_green `int`
- m_blue `int`


# GuildColorBorder.dbc

0x4 fields, 0x8 bytes

- m_colorID `int`
- m_red `int`
- m_green `int`
- m_blue `int`


# GuildColorEmblem.dbc

0x4 fields, 0x8 bytes

- m_colorID `int`
- m_red `int`
- m_green `int`
- m_blue `int`


# GuildPerkSpells.dbc

0x3 fields, 0xc bytes

- m_id `int`
- m_guildLevel `int`
- m_spellID `int`


# HelmetAnimScaling.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_helmetGeosetVisDataID `int`
- m_raceID `int`
- m_amount `float`


# HelmetGeosetVisData.dbc

0x2 fields, 0x20 bytes

- m_ID `int`
- m_hideGeoset_0 `int`
- m_hideGeoset_1 `int`
- m_hideGeoset_2 `int`
- m_hideGeoset_3 `int`
- m_hideGeoset_4 `int`
- m_hideGeoset_5 `int`
- m_hideGeoset_6 `int`


# HolidayDescriptions.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_description_lang `string`


# HolidayNames.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_name_lang `string`


# Holidays.dbc

0xc fields, 0xdc bytes

- m_ID `int`
- m_duration_0 `int`
- m_duration_1 `int`
- m_duration_2 `int`
- m_duration_3 `int`
- m_duration_4 `int`
- m_duration_5 `int`
- m_duration_6 `int`
- m_duration_7 `int`
- m_duration_8 `int`
- m_duration_9 `int`
- m_date_0 `int`
- m_date_1 `int`
- m_date_2 `int`
- m_date_3 `int`
- m_date_4 `int`
- m_date_5 `int`
- m_date_6 `int`
- m_date_7 `int`
- m_date_8 `int`
- m_date_9 `int`
- m_date_10 `int`
- m_date_11 `int`
- m_date_12 `int`
- m_date_13 `int`
- m_date_14 `int`
- m_date_15 `int`
- m_date_16 `int`
- m_date_17 `int`
- m_date_18 `int`
- m_date_19 `int`
- m_date_20 `int`
- m_date_21 `int`
- m_date_22 `int`
- m_date_23 `int`
- m_date_24 `int`
- m_date_25 `int`
- m_region `int`
- m_looping `int`
- m_calendarFlags_0 `int`
- m_calendarFlags_1 `int`
- m_calendarFlags_2 `int`
- m_calendarFlags_3 `int`
- m_calendarFlags_4 `int`
- m_calendarFlags_5 `int`
- m_calendarFlags_6 `int`
- m_calendarFlags_7 `int`
- m_calendarFlags_8 `int`
- m_calendarFlags_9 `int`
- m_holidayNameID `int`
- m_holidayDescriptionID `int`
- m_textureFilename `string`
- m_priority `int`
- m_calendarFilterType `int`
- m_flags `int`


# ImportPriceArmor.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_ClothModifier `float`
- m_LeatherModifier `float`
- m_ChainModifier `float`
- m_PlateModifier `float`


# ImportPriceQuality.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_data `float`


# ImportPriceShield.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_data `float`


# ImportPriceWeapon.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_data `float`


# ItemArmorQuality.dbc

0x3 fields, 0x24 bytes

- m_ID `int`
- m_qualitymod_0 `float`
- m_qualitymod_1 `float`
- m_qualitymod_2 `float`
- m_qualitymod_3 `float`
- m_qualitymod_4 `float`
- m_qualitymod_5 `float`
- m_qualitymod_6 `float`
- m_itemLevel `int`


# ItemArmorShield.dbc

0x3 fields, 0x24 bytes

- m_ID `int`
- m_itemLevel `int`
- m_quality_0 `float`
- m_quality_1 `float`
- m_quality_2 `float`
- m_quality_3 `float`
- m_quality_4 `float`
- m_quality_5 `float`
- m_quality_6 `float`


# ItemArmorTotal.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_itemLevel `int`
- m_cloth `float`
- m_leather `float`
- m_mail `float`
- m_plate `float`


# ItemBagFamily.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_name_lang `string`


# ItemClass.dbc

0x4 fields, 0x10 bytes

- m_classID `int`
- m_flags `int`
- m_priceModifier `float`
- m_className_lang `string`


# ItemDamageAmmo.dbc

0x3 fields, 0x24 bytes

- m_ID `int`
- m_quality_0 `float`
- m_quality_1 `float`
- m_quality_2 `float`
- m_quality_3 `float`
- m_quality_4 `float`
- m_quality_5 `float`
- m_quality_6 `float`
- m_itemLevel `int`


# ItemDamageOneHandCaster.dbc

0x3 fields, 0x24 bytes

- m_ID `int`
- m_quality_0 `float`
- m_quality_1 `float`
- m_quality_2 `float`
- m_quality_3 `float`
- m_quality_4 `float`
- m_quality_5 `float`
- m_quality_6 `float`
- m_itemLevel `int`


# ItemDamageOneHand.dbc

0x3 fields, 0x24 bytes

- m_ID `int`
- m_quality_0 `float`
- m_quality_1 `float`
- m_quality_2 `float`
- m_quality_3 `float`
- m_quality_4 `float`
- m_quality_5 `float`
- m_quality_6 `float`
- m_itemLevel `int`


# ItemDamageRanged.dbc

0x3 fields, 0x24 bytes

- m_ID `int`
- m_quality_0 `float`
- m_quality_1 `float`
- m_quality_2 `float`
- m_quality_3 `float`
- m_quality_4 `float`
- m_quality_5 `float`
- m_quality_6 `float`
- m_itemLevel `int`


# ItemDamageThrown.dbc

0x3 fields, 0x24 bytes

- m_ID `int`
- m_quality_0 `float`
- m_quality_1 `float`
- m_quality_2 `float`
- m_quality_3 `float`
- m_quality_4 `float`
- m_quality_5 `float`
- m_quality_6 `float`
- m_itemLevel `int`


# ItemDamageTwoHandCaster.dbc

0x3 fields, 0x24 bytes

- m_ID `int`
- m_quality_0 `float`
- m_quality_1 `float`
- m_quality_2 `float`
- m_quality_3 `float`
- m_quality_4 `float`
- m_quality_5 `float`
- m_quality_6 `float`
- m_itemLevel `int`


# ItemDamageTwoHand.dbc

0x3 fields, 0x24 bytes

- m_ID `int`
- m_quality_0 `float`
- m_quality_1 `float`
- m_quality_2 `float`
- m_quality_3 `float`
- m_quality_4 `float`
- m_quality_5 `float`
- m_quality_6 `float`
- m_itemLevel `int`


# ItemDamageWand.dbc

0x3 fields, 0x24 bytes

- m_ID `int`
- m_quality_0 `float`
- m_quality_1 `float`
- m_quality_2 `float`
- m_quality_3 `float`
- m_quality_4 `float`
- m_quality_5 `float`
- m_quality_6 `float`
- m_itemLevel `int`


# ItemDisenchantLoot.dbc

0x7 fields, 0x1c bytes

- m_ID `int`
- m_class `int`
- m_subclass `int`
- m_quality `int`
- m_minLevel `int`
- m_maxLevel `int`
- m_skillRequired `int`


# ItemDisplayInfo.dbc

0xa fields, 0x5c bytes

- m_ID `int`
- m_modelName_0 `string`
- m_modelName_1 `string`
- m_modelTexture_0 `string`
- m_modelTexture_1 `string`
- m_geosetGroup_0 `int`
- m_geosetGroup_1 `int`
- m_geosetGroup_2 `int`
- m_flags `int`
- m_spellVisualID `int`
- m_helmetGeosetVis_0 `int`
- m_helmetGeosetVis_1 `int`
- m_texture_0 `string`
- m_texture_1 `string`
- m_texture_2 `string`
- m_texture_3 `string`
- m_texture_4 `string`
- m_texture_5 `string`
- m_texture_6 `string`
- m_texture_7 `string`
- m_texture_8 `string`
- m_itemVisual `int`
- m_particleColorID `int`


# ItemGroupSounds.dbc

0x2 fields, 0x14 bytes

- m_ID `int`
- m_sound_0 `int`
- m_sound_1 `int`
- m_sound_2 `int`
- m_sound_3 `int`


# ItemLimitCategory.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_name_lang `string`
- m_quantity `int`
- m_flags `int`


# ItemNameDescription.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_description_lang `string`
- m_color `int`


# ItemPetFood.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_Name_lang `string`


# ItemPriceBase.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_itemLevel `int`
- m_armor `float`
- m_weapon `float`


# ItemPurchaseGroup.dbc

0x3 fields, 0x28 bytes

- m_ID `int`
- m_itemID_0 `int`
- m_itemID_1 `int`
- m_itemID_2 `int`
- m_itemID_3 `int`
- m_itemID_4 `int`
- m_itemID_5 `int`
- m_itemID_6 `int`
- m_itemID_7 `int`
- m_name_lang `string`


# ItemRandomProperties.dbc

0x4 fields, 0x20 bytes

- m_ID `int`
- m_Name `string`
- m_Enchantment_0 `int`
- m_Enchantment_1 `int`
- m_Enchantment_2 `int`
- m_Enchantment_3 `int`
- m_Enchantment_4 `int`
- m_name_lang `string`


# ItemRandomSuffix.dbc

0x5 fields, 0x34 bytes

- m_ID `int`
- m_name_lang `string`
- m_internalName `string`
- m_enchantment_0 `int`
- m_enchantment_1 `int`
- m_enchantment_2 `int`
- m_enchantment_3 `int`
- m_enchantment_4 `int`
- m_allocationPct_0 `int`
- m_allocationPct_1 `int`
- m_allocationPct_2 `int`
- m_allocationPct_3 `int`
- m_allocationPct_4 `int`


# ItemSet.dbc

0x5 fields, 0x54 bytes

- m_ID `int`
- m_name_lang `string`
- m_itemID_0 `int`
- m_itemID_1 `int`
- m_itemID_2 `int`
- m_itemID_3 `int`
- m_itemID_4 `int`
- m_itemID_5 `int`
- m_itemID_6 `int`
- m_itemID_7 `int`
- m_itemID_8 `int`
- m_itemID_9 `int`
- m_itemID_10 `int`
- m_itemID_11 `int`
- m_itemID_12 `int`
- m_itemID_13 `int`
- m_itemID_14 `int`
- m_itemID_15 `int`
- m_itemID_16 `int`
- m_requiredSkill `int`
- m_requiredSkillRank `int`


# ItemSetSpell.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_itemSetID `int`
- m_spellID `int`
- m_threshold `int`
- m_chrSpecID `int`


# ItemSpecOverride.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_itemID `int`
- m_specID `int`


# ItemSpec.dbc

0x7 fields, 0x1c bytes

- m_ID `int`
- m_minLevel `int`
- m_maxLevel `int`
- m_itemType `int`
- m_primaryStat `int`
- m_secondaryStat `int`
- m_specializationID `int`


# ItemSubClassMask.dbc

0x3 fields, 0x10 bytes

- m_classID `int`
- m_mask `int`
- m_name_lang `string`


# ItemSubClass.dbc

0xc fields, 0x34 bytes

- m_classID `int`
- m_subClassID `int`
- m_prerequisiteProficiency `int`
- m_postrequisiteProficiency `int`
- m_flags `int`
- m_displayFlags `int`
- m_weaponParrySeq `int`
- m_weaponReadySeq `int`
- m_weaponAttackSeq `int`
- m_WeaponSwingSize `int`
- m_displayName_lang `string`
- m_verboseName_lang `string`


# ItemUpgradePath.dbc

0x1 fields, 0x4 bytes

- m_id `int`


# ItemVisualEffects.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_Model `string`


# ItemVisuals.dbc

0x2 fields, 0x18 bytes

- m_ID `int`
- m_Slot_0 `int`
- m_Slot_1 `int`
- m_Slot_2 `int`
- m_Slot_3 `int`
- m_Slot_4 `int`


# JournalEncounterCreature.dbc

0x7 fields, 0x1c bytes

- m_ID `int`
- m_journalEncounterID `int`
- m_creatureDisplayInfoID `int`
- m_orderIndex `int`
- m_fileDataID `int`
- m_name_lang `string`
- m_description_lang `string`


# JournalEncounterItem.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_journalEncounterID `int`
- m_itemID `int`
- m_difficultyMask `int`
- m_factionMask `int`
- m_flags `int`


# JournalEncounter.dbc

0xb fields, 0x30 bytes

- m_ID `int`
- m_dungeonMapID `int`
- m_worldMapAreaID `int`
- m_map_x `float`
- m_map_y `float`
- m_firstSectionID `int`
- m_journalInstanceID `int`
- m_orderIndex `int`
- m_difficultyMask `int`
- m_name_lang `string`
- m_description_lang `string`
- m_flags `int`


# JournalEncounterSection.dbc

0xf fields, 0x3c bytes

- m_ID `int`
- m_journalEncounterID `int`
- m_nextSiblingSectionID `int`
- m_firstChildSectionID `int`
- m_parentSectionID `int`
- m_orderIndex `int`
- m_type `int`
- m_flags `int`
- m_iconFlags `int`
- m_title_lang `string`
- m_bodyText_lang `string`
- m_difficultyMask `int`
- m_iconCreatureDisplayInfoID `int`
- m_spellID `int`
- m_iconFileDataID `int`


# JournalEncounterXDifficulty.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_journalEncounterID `int`
- m_difficultyID `int`


# JournalInstance.dbc

0x9 fields, 0x24 bytes

- m_ID `int`
- m_mapID `int`
- m_areaID `int`
- m_buttonFiledataID `int`
- m_buttonSmallFileDataID `int`
- m_backgroundFiledataID `int`
- m_loreFileDataID `int`
- m_name_lang `string`
- m_description_lang `string`


# JournalItemXDifficulty.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_journalEncounterItemID `int`
- m_difficultyID `int`


# JournalSectionXDifficulty.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_journalEncounterSectionID `int`
- m_difficultyID `int`


# JournalTier.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_name_lang `string`


# JournalTierXInstance.dbc

0x2 fields, 0x8 bytes

- m_journalTierID `int`
- m_journalInstanceID `int`


# Languages.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_name_lang `string`


# LanguageWords.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_languageID `int`
- m_word `string`


# LfgDungeonExpansion.dbc

0x8 fields, 0x20 bytes

- m_ID `int`
- m_lfg_id `int`
- m_expansion_level `int`
- m_random_id `int`
- m_hard_level_min `int`
- m_hard_level_max `int`
- m_target_level_min `int`
- m_target_level_max `int`


# LfgDungeonGroup.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_name_lang `string`
- m_order_index `int`
- m_parent_group_id `int`
- m_typeid `int`


# LfgDungeonsGroupingMap.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_lfgDungeonsID `int`
- m_random_lfgDungeonsID `int`
- m_group_id `int`


# LfgDungeons.dbc

0x1d fields, 0x74 bytes

- m_ID `int`
- m_name_lang `string`
- m_minLevel `int`
- m_maxLevel `int`
- m_target_level `int`
- m_target_level_min `int`
- m_target_level_max `int`
- m_mapID `int`
- m_difficultyID `int`
- m_flags `int`
- m_typeID `int`
- m_faction `int`
- m_textureFilename `string`
- m_expansionLevel `int`
- m_order_index `int`
- m_group_id `int`
- m_description_lang `string`
- m_random_id `int`
- m_count_tank `int`
- m_count_healer `int`
- m_count_damage `int`
- m_min_count_tank `int`
- m_min_count_healer `int`
- m_min_count_damage `int`
- m_scenarioID `int`
- m_subtype `int`
- m_bonus_reputation_amount `int`
- m_mentorCharLevel `int`
- m_mentorItemLevel `int`


# LoadingScreens.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_name `string`
- m_fileName `string`
- m_hasWideScreen `int`


# LoadingScreenTaxiSplines.dbc

0x6 fields, 0x60 bytes

- m_ID `int`
- m_PathID `int`
- m_Locx_0 `float`
- m_Locx_1 `float`
- m_Locx_2 `float`
- m_Locx_3 `float`
- m_Locx_4 `float`
- m_Locx_5 `float`
- m_Locx_6 `float`
- m_Locx_7 `float`
- m_Locx_8 `float`
- m_Locx_9 `float`
- m_Locy_0 `float`
- m_Locy_1 `float`
- m_Locy_2 `float`
- m_Locy_3 `float`
- m_Locy_4 `float`
- m_Locy_5 `float`
- m_Locy_6 `float`
- m_Locy_7 `float`
- m_Locy_8 `float`
- m_Locy_9 `float`
- m_LegIndex `int`
- m_LoadingScreenID `int`


# Lock.dbc

0x5 fields, 0x84 bytes

- m_ID `int`
- m_Type_0 `int`
- m_Type_1 `int`
- m_Type_2 `int`
- m_Type_3 `int`
- m_Type_4 `int`
- m_Type_5 `int`
- m_Type_6 `int`
- m_Type_7 `int`
- m_Index_0 `int`
- m_Index_1 `int`
- m_Index_2 `int`
- m_Index_3 `int`
- m_Index_4 `int`
- m_Index_5 `int`
- m_Index_6 `int`
- m_Index_7 `int`
- m_Skill_0 `int`
- m_Skill_1 `int`
- m_Skill_2 `int`
- m_Skill_3 `int`
- m_Skill_4 `int`
- m_Skill_5 `int`
- m_Skill_6 `int`
- m_Skill_7 `int`
- m_Action_0 `int`
- m_Action_1 `int`
- m_Action_2 `int`
- m_Action_3 `int`
- m_Action_4 `int`
- m_Action_5 `int`
- m_Action_6 `int`
- m_Action_7 `int`


# LockType.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_name_lang `string`
- m_resourceName_lang `string`
- m_verb_lang `string`
- m_cursorName `string`


# MailTemplate.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_subject_lang `string`
- m_body_lang `string`


# ManifestInterfaceActionIcon.dbc

0x1 fields, 0x4 bytes

- m_ID `int`


# ManifestInterfaceData.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_FilePath `string`
- m_FileName `string`


# ManifestInterfaceItemIcon.dbc

0x1 fields, 0x4 bytes

- m_ID `int`


# ManifestInterfaceTOCData.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_FilePath `string`


# MapDifficulty.dbc

0x7 fields, 0x1c bytes

- m_ID `int`
- m_mapID `int`
- m_difficultyID `int`
- m_message_lang `string`
- m_raidDuration `int`
- m_maxPlayers `int`
- m_lockID `int`


# Material.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_flags `int`
- m_foleySoundID `int`
- m_sheatheSoundID `int`
- m_unsheatheSoundID `int`


# MinorTalent.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_chrSpecializationID `int`
- m_spellID `int`
- m_orderIndex `int`


# ModifierTree.dbc

0x7 fields, 0x1c bytes

- m_ID `int`
- m_type `int`
- m_asset `int`
- m_secondaryAsset `int`
- m_operator `int`
- m_amount `int`
- m_parent `int`


# MountCapability.dbc

0x8 fields, 0x20 bytes

- m_ID `int`
- m_flags `int`
- m_reqRidingSkill `int`
- m_reqAreaID `int`
- m_reqSpellAuraID `int`
- m_reqSpellKnownID `int`
- m_modSpellAuraID `int`
- m_reqMapID `int`


# MountType.dbc

0x2 fields, 0x64 bytes

- m_ID `int`
- m_capability_0 `int`
- m_capability_1 `int`
- m_capability_2 `int`
- m_capability_3 `int`
- m_capability_4 `int`
- m_capability_5 `int`
- m_capability_6 `int`
- m_capability_7 `int`
- m_capability_8 `int`
- m_capability_9 `int`
- m_capability_10 `int`
- m_capability_11 `int`
- m_capability_12 `int`
- m_capability_13 `int`
- m_capability_14 `int`
- m_capability_15 `int`
- m_capability_16 `int`
- m_capability_17 `int`
- m_capability_18 `int`
- m_capability_19 `int`
- m_capability_20 `int`
- m_capability_21 `int`
- m_capability_22 `int`
- m_capability_23 `int`


# MovieFileData.dbc

0x2 fields, 0x8 bytes

- m_FileDataID `int`
- m_resolution `int`


# MovieOverlays.dbc

0x4 fields, 0x14 bytes

- m_movieID `int`
- m_localeMask `int`
- m_overlayRangeBegin `int`
- m_overlayRangeEnd `int`


# Movie.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_volume `int`
- m_keyID `int`
- m_audioFileDataID `int`
- m_subtitleFileDataID `int`


# MovieVariation.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_movieID `int`
- m_fileDataID `int`
- m_OverlayFileDataID `int`


# NameGen.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_name `string`
- m_raceID `int`
- m_sex `int`


# NamesProfanity.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_Name `string`
- m_Language `int`


# NamesReservedLocale.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_Name `string`
- m_LocaleMask `int`


# NamesReserved.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_Name `string`


# NPCSounds.dbc

0x2 fields, 0x14 bytes

- m_ID `int`
- m_SoundID_0 `int`
- m_SoundID_1 `int`
- m_SoundID_2 `int`
- m_SoundID_3 `int`


# ObjectEffectGroup.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_name `string`


# ObjectEffectModifier.dbc

0x5 fields, 0x20 bytes

- m_ID `int`
- m_inputType `int`
- m_mapType `int`
- m_outputType `int`
- m_param_0 `float`
- m_param_1 `float`
- m_param_2 `float`
- m_param_3 `float`


# ObjectEffectPackageElem.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_objectEffectPackageID `int`
- m_objectEffectGroupID `int`
- m_stateType `int`


# ObjectEffectPackage.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_name `string`


# ObjectEffect.dbc

0xa fields, 0x30 bytes

- m_ID `int`
- m_name `string`
- m_objectEffectGroupID `int`
- m_triggerType `int`
- m_eventType `int`
- m_effectRecType `int`
- m_effectRecID `int`
- m_attachment `int`
- m_offset_x `float`
- m_offset_y `float`
- m_offset_z `float`
- m_objectEffectModifierID `int`


# OverrideSpellData.dbc

0x4 fields, 0x34 bytes

- m_ID `int`
- m_spells_0 `int`
- m_spells_1 `int`
- m_spells_2 `int`
- m_spells_3 `int`
- m_spells_4 `int`
- m_spells_5 `int`
- m_spells_6 `int`
- m_spells_7 `int`
- m_spells_8 `int`
- m_spells_9 `int`
- m_flags `int`
- m_playerActionbarFileDataID `int`


# Package.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_icon `string`
- m_cost `int`
- m_name_lang `string`


# PageTextMaterial.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_name `string`


# PaperDollItemFrame.dbc

0x3 fields, 0x10 bytes

- m_ItemButtonName `string`
- m_SlotIcon `string`
- m_SlotNumber `int`


# ParticleColor.dbc

0x4 fields, 0x28 bytes

- m_ID `int`
- m_start_0 `int`
- m_start_1 `int`
- m_start_2 `int`
- m_mid_0 `int`
- m_mid_1 `int`
- m_mid_2 `int`
- m_end_0 `int`
- m_end_1 `int`
- m_end_2 `int`


# Phase.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_name `string`
- m_flags `int`


# PhaseShiftZoneSounds.dbc

0xe fields, 0x38 bytes

- m_ID `int`
- m_AreaID `int`
- m_WMOAreaID `int`
- m_PhaseID `int`
- m_PhaseGroupID `int`
- m_PhaseUseFlags `int`
- m_ZoneIntroMusicID `int`
- m_ZoneMusicID `int`
- m_SoundAmbienceID `int`
- m_SoundProviderPreferencesID `int`
- m_UWZoneIntroMusicID `int`
- m_UWZoneMusicID `int`
- m_UWSoundAmbienceID `int`
- m_UWSoundProviderPreferencesID `int`


# PhaseXPhaseGroup.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_phaseID `int`
- m_phaseGroupID `int`


# PlayerCondition.dbc

0x4c fields, 0x220 bytes

- m_ID `int`
- m_flags `int`
- m_minLevel `int`
- m_maxLevel `int`
- m_raceMask `int`
- m_classMask `int`
- m_gender `int`
- m_nativeGender `int`
- m_skillID_0 `int`
- m_skillID_1 `int`
- m_skillID_2 `int`
- m_skillID_3 `int`
- m_minSkill_0 `int`
- m_minSkill_1 `int`
- m_minSkill_2 `int`
- m_minSkill_3 `int`
- m_maxSkill_0 `int`
- m_maxSkill_1 `int`
- m_maxSkill_2 `int`
- m_maxSkill_3 `int`
- m_skillLogic `int`
- m_languageID `int`
- m_minLanguage `int`
- m_maxLanguage `int`
- m_minFactionID_0 `int`
- m_minFactionID_1 `int`
- m_minFactionID_2 `int`
- m_maxFactionID `int`
- m_minReputation_0 `int`
- m_minReputation_1 `int`
- m_minReputation_2 `int`
- m_maxReputation `int`
- m_reputationLogic `int`
- m_minPVPRank `int`
- m_maxPVPRank `int`
- m_pvpMedal `int`
- m_prevQuestLogic `int`
- m_prevQuestID_0 `int`
- m_prevQuestID_1 `int`
- m_prevQuestID_2 `int`
- m_prevQuestID_3 `int`
- m_currQuestLogic `int`
- m_currQuestID_0 `int`
- m_currQuestID_1 `int`
- m_currQuestID_2 `int`
- m_currQuestID_3 `int`
- m_currentCompletedQuestLogic `int`
- m_currentCompletedQuestID_0 `int`
- m_currentCompletedQuestID_1 `int`
- m_currentCompletedQuestID_2 `int`
- m_currentCompletedQuestID_3 `int`
- m_spellLogic `int`
- m_spellID_0 `int`
- m_spellID_1 `int`
- m_spellID_2 `int`
- m_spellID_3 `int`
- m_itemLogic `int`
- m_itemID_0 `int`
- m_itemID_1 `int`
- m_itemID_2 `int`
- m_itemID_3 `int`
- m_itemCount_0 `int`
- m_itemCount_1 `int`
- m_itemCount_2 `int`
- m_itemCount_3 `int`
- m_itemFlags `int`
- m_explored_0 `int`
- m_explored_1 `int`
- m_time_0 `int`
- m_time_1 `int`
- m_auraSpellLogic `int`
- m_auraSpellID_0 `int`
- m_auraSpellID_1 `int`
- m_auraSpellID_2 `int`
- m_auraSpellID_3 `int`
- m_worldStateExpressionID `int`
- m_weatherID `int`
- m_partyStatus `int`
- m_lifetimeMaxPVPRank `int`
- m_achievementLogic `int`
- m_achievement_0 `int`
- m_achievement_1 `int`
- m_achievement_2 `int`
- m_achievement_3 `int`
- m_lfgLogic `int`
- m_lfgStatus_0 `int`
- m_lfgStatus_1 `int`
- m_lfgStatus_2 `int`
- m_lfgStatus_3 `int`
- m_lfgCompare_0 `int`
- m_lfgCompare_1 `int`
- m_lfgCompare_2 `int`
- m_lfgCompare_3 `int`
- m_lfgValue_0 `int`
- m_lfgValue_1 `int`
- m_lfgValue_2 `int`
- m_lfgValue_3 `int`
- m_areaLogic `int`
- m_areaID_0 `int`
- m_areaID_1 `int`
- m_areaID_2 `int`
- m_areaID_3 `int`
- m_currencyLogic `int`
- m_currencyID_0 `int`
- m_currencyID_1 `int`
- m_currencyID_2 `int`
- m_currencyID_3 `int`
- m_currencyCount_0 `int`
- m_currencyCount_1 `int`
- m_currencyCount_2 `int`
- m_currencyCount_3 `int`
- m_questKillID `int`
- m_questKillLogic `int`
- m_questKillMonster_0 `int`
- m_questKillMonster_1 `int`
- m_questKillMonster_2 `int`
- m_questKillMonster_3 `int`
- m_minExpansionLevel `int`
- m_maxExpansionLevel `int`
- m_minExpansionTier `int`
- m_maxExpansionTier `int`
- m_minGuildLevel `int`
- m_maxGuildLevel `int`
- m_phaseUseFlags `int`
- m_phaseID `int`
- m_phaseGroupID `int`
- m_minAvgItemLevel `int`
- m_maxAvgItemLevel `int`
- m_minAvgEquippedItemLevel `int`
- m_maxAvgEquippedItemLevel `int`
- m_chrSpecializationIndex `int`
- m_chrSpecializationRole `int`
- m_failure_description_lang `string`
- m_powerType `int`
- m_powerTypeComp `int`
- m_powerTypeValue `int`


# PowerDisplay.dbc

0x6 fields, 0x10 bytes

- m_ID `int`
- m_actualType `int`
- m_globalStringBaseTag `string`
- m_red `int`
- m_green `int`
- m_blue `int`


# PvpDifficulty.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_mapID `int`
- m_rangeIndex `int`
- m_minLevel `int`
- m_maxLevel `int`


# QuestFactionReward.dbc

0x2 fields, 0x2c bytes

- m_ID `int`
- m_Difficulty_0 `int`
- m_Difficulty_1 `int`
- m_Difficulty_2 `int`
- m_Difficulty_3 `int`
- m_Difficulty_4 `int`
- m_Difficulty_5 `int`
- m_Difficulty_6 `int`
- m_Difficulty_7 `int`
- m_Difficulty_8 `int`
- m_Difficulty_9 `int`


# QuestFeedbackEffect.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_fileDataID `int`
- m_attachPoint `int`
- m_minimapobject `int`
- m_priority `int`
- m_flags `int`


# QuestInfo.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_InfoName_lang `string`


# QuestMoneyReward.dbc

0x2 fields, 0x2c bytes

- m_ID `int`
- m_difficulty_0 `int`
- m_difficulty_1 `int`
- m_difficulty_2 `int`
- m_difficulty_3 `int`
- m_difficulty_4 `int`
- m_difficulty_5 `int`
- m_difficulty_6 `int`
- m_difficulty_7 `int`
- m_difficulty_8 `int`
- m_difficulty_9 `int`


# QuestPOIBlob.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_NumPoints `int`
- m_MapID `int`
- m_WorldMapAreaID `int`


# QuestPOIPoint.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_X `int`
- m_Y `int`
- m_QuestPOIBlobID `int`


# QuestSort.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_SortName_lang `string`


# QuestV2.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_UniqueBitFlag `int`


# QuestXP.dbc

0x2 fields, 0x2c bytes

- m_ID `int`
- m_difficulty_0 `int`
- m_difficulty_1 `int`
- m_difficulty_2 `int`
- m_difficulty_3 `int`
- m_difficulty_4 `int`
- m_difficulty_5 `int`
- m_difficulty_6 `int`
- m_difficulty_7 `int`
- m_difficulty_8 `int`
- m_difficulty_9 `int`


# RacialMounts.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_race `int`
- m_spell_id `int`


# RandPropPoints.dbc

0x4 fields, 0x40 bytes

- m_ID `int`
- m_Epic_0 `int`
- m_Epic_1 `int`
- m_Epic_2 `int`
- m_Epic_3 `int`
- m_Epic_4 `int`
- m_Superior_0 `int`
- m_Superior_1 `int`
- m_Superior_2 `int`
- m_Superior_3 `int`
- m_Superior_4 `int`
- m_Good_0 `int`
- m_Good_1 `int`
- m_Good_2 `int`
- m_Good_3 `int`
- m_Good_4 `int`


# ResearchBranch.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_name_lang `string`
- m_researchFieldID `int`
- m_currencyID `int`
- m_texture `string`
- m_itemID `int`


# ResearchField.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_name_lang `string`
- m_slot `int`


# ResearchProject.dbc

0x9 fields, 0x24 bytes

- m_ID `int`
- m_name_lang `string`
- m_description_lang `string`
- m_rarity `int`
- m_researchBranchID `int`
- m_spellID `int`
- m_numSockets `int`
- m_texture `string`
- m_requiredWeight `int`


# ResearchSite.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_mapID `int`
- m_QuestPOIBlobID `int`
- m_name_lang `string`
- m_areaPOIIconEnum `int`


# Resistances.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_Flags `int`
- m_FizzleSoundID `int`
- m_name_lang `string`


# RulesetRaidOverride.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_mapID `int`
- m_difficultyID `int`
- m_rulesetID `int`
- m_sharedLock `int`
- m_raidduration `int`


# ScalingStatDistribution.dbc

0x5 fields, 0x5c bytes

- m_ID `int`
- m_statID_0 `int`
- m_statID_1 `int`
- m_statID_2 `int`
- m_statID_3 `int`
- m_statID_4 `int`
- m_statID_5 `int`
- m_statID_6 `int`
- m_statID_7 `int`
- m_statID_8 `int`
- m_statID_9 `int`
- m_bonus_0 `int`
- m_bonus_1 `int`
- m_bonus_2 `int`
- m_bonus_3 `int`
- m_bonus_4 `int`
- m_bonus_5 `int`
- m_bonus_6 `int`
- m_bonus_7 `int`
- m_bonus_8 `int`
- m_bonus_9 `int`
- m_minlevel `int`
- m_maxlevel `int`


# ScalingStatValues.dbc

0x19 fields, 0xc4 bytes

- m_ID `int`
- m_charlevel `int`
- m_effectiveLevel `int`
- m_weaponDPS1H `int`
- m_weaponDPS2H `int`
- m_spellcasterDPS1H `int`
- m_spellcasterDPS2H `int`
- m_rangedDPS `int`
- m_wandDPS `int`
- m_spellPower `int`
- m_budgetPrimary `int`
- m_budgetSecondary `int`
- m_budgetTertiary `int`
- m_budgetSub `int`
- m_budgetTrivial `int`
- m_armorShoulder_0 `int`
- m_armorShoulder_1 `int`
- m_armorShoulder_2 `int`
- m_armorShoulder_3 `int`
- m_armorChest_0 `int`
- m_armorChest_1 `int`
- m_armorChest_2 `int`
- m_armorChest_3 `int`
- m_armorHead_0 `int`
- m_armorHead_1 `int`
- m_armorHead_2 `int`
- m_armorHead_3 `int`
- m_armorLegs_0 `int`
- m_armorLegs_1 `int`
- m_armorLegs_2 `int`
- m_armorLegs_3 `int`
- m_armorFeet_0 `int`
- m_armorFeet_1 `int`
- m_armorFeet_2 `int`
- m_armorFeet_3 `int`
- m_armorWaist_0 `int`
- m_armorWaist_1 `int`
- m_armorWaist_2 `int`
- m_armorWaist_3 `int`
- m_armorHands_0 `int`
- m_armorHands_1 `int`
- m_armorHands_2 `int`
- m_armorHands_3 `int`
- m_armorWrists_0 `int`
- m_armorWrists_1 `int`
- m_armorWrists_2 `int`
- m_armorWrists_3 `int`
- m_armorBack `int`
- m_armorShield `int`


# ScenarioEventEntry.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_triggerType `int`
- m_triggerAsset `int`


# Scenario.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_name_lang `string`
- m_flags `int`


# ScenarioStep.dbc

0xa fields, 0x28 bytes

- m_ID `int`
- m_criteriatreeid `int`
- m_scenarioID `int`
- m_orderIndex `int`
- m_description_lang `string`
- m_title_lang `string`
- m_flags `int`
- m_relatedStep `int`
- m_supersedes `int`
- m_rewardQuestID `int`


# ScreenEffect.dbc

0xc fields, 0x3c bytes

- m_id `int`
- m_name `string`
- m_effect `int`
- m_param_0 `int`
- m_param_1 `int`
- m_param_2 `int`
- m_param_3 `int`
- m_lightParamsID `int`
- m_lightParamsFadeIn `int`
- m_lightParamsFadeOut `int`
- m_lightFlags `int`
- m_soundAmbienceID `int`
- m_zoneMusicID `int`
- m_timeOfDayOverride `int`
- m_effectMask `int`


# ScreenLocation.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_name `string`


# ServerMessages.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_Text_lang `string`


# SkillLineAbility.dbc

0xd fields, 0x34 bytes

- m_ID `int`
- m_skillLine `int`
- m_spell `int`
- m_raceMask `int`
- m_classMask `int`
- m_minSkillLineRank `int`
- m_supercedesSpell `int`
- m_acquireMethod `int`
- m_trivialSkillLineRankHigh `int`
- m_trivialSkillLineRankLow `int`
- m_numSkillUps `int`
- m_uniqueBit `int`
- m_tradeSkillCategoryID `int`


# SkillLineAbilitySortedSpell.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_spell `int`


# SkillLine.dbc

0x9 fields, 0x24 bytes

- m_ID `int`
- m_categoryID `int`
- m_displayName_lang `string`
- m_description_lang `string`
- m_spellIconID `int`
- m_alternateVerb_lang `string`
- m_canLink `int`
- m_parentSkillLineID `int`
- m_flags `int`


# SkillRaceClassInfo.dbc

0x8 fields, 0x20 bytes

- m_ID `int`
- m_skillID `int`
- m_raceMask `int`
- m_classMask `int`
- m_flags `int`
- m_availability `int`
- m_minLevel `int`
- m_skillTierID `int`


# SkillTiers.dbc

0x2 fields, 0x44 bytes

- m_ID `int`
- m_value_0 `int`
- m_value_1 `int`
- m_value_2 `int`
- m_value_3 `int`
- m_value_4 `int`
- m_value_5 `int`
- m_value_6 `int`
- m_value_7 `int`
- m_value_8 `int`
- m_value_9 `int`
- m_value_10 `int`
- m_value_11 `int`
- m_value_12 `int`
- m_value_13 `int`
- m_value_14 `int`
- m_value_15 `int`


# SoundAmbienceFlavor.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_SoundAmbienceID `int`
- m_SoundEntriesIDDay `int`
- m_SoundEntriesIDNight `int`


# SoundAmbience.dbc

0x3 fields, 0x10 bytes

- m_ID `int`
- m_AmbienceID_0 `int`
- m_AmbienceID_1 `int`
- m_flags `int`


# SoundFilterElem.dbc

0x5 fields, 0x34 bytes

- m_ID `int`
- m_soundFilterID `int`
- m_orderIndex `int`
- m_filterType `int`
- m_params_0 `float`
- m_params_1 `float`
- m_params_2 `float`
- m_params_3 `float`
- m_params_4 `float`
- m_params_5 `float`
- m_params_6 `float`
- m_params_7 `float`
- m_params_8 `float`


# SoundFilter.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_name `string`


# SoundOverride.dbc

0x7 fields, 0x1c bytes

- m_ID `int`
- m_WowEditLock `int`
- m_WowEditLockUser `string`
- m_ZoneIntroMusicID `int`
- m_ZoneMusicID `int`
- m_SoundAmbienceID `int`
- m_SoundProviderPreferencesID `int`


# SoundProviderPreferences.dbc

0x18 fields, 0x60 bytes

- m_ID `int`
- m_Description `string`
- m_Flags `int`
- m_EAXEnvironmentSelection `int`
- m_EAXDecayTime `float`
- m_EAX2EnvironmentSize `float`
- m_EAX2EnvironmentDiffusion `float`
- m_EAX2Room `int`
- m_EAX2RoomHF `int`
- m_EAX2DecayHFRatio `float`
- m_EAX2Reflections `int`
- m_EAX2ReflectionsDelay `float`
- m_EAX2Reverb `int`
- m_EAX2ReverbDelay `float`
- m_EAX2RoomRolloff `float`
- m_EAX2AirAbsorption `float`
- m_EAX3RoomLF `int`
- m_EAX3DecayLFRatio `float`
- m_EAX3EchoTime `float`
- m_EAX3EchoDepth `float`
- m_EAX3ModulationTime `float`
- m_EAX3ModulationDepth `float`
- m_EAX3HFReference `float`
- m_EAX3LFReference `float`


# SpamMessages.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_text `string`


# SpecializationSpells.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_specID `int`
- m_spellID `int`
- m_overridesSpellID `int`
- m_description_lang `string`


# SpellActivationOverlay.dbc

0x9 fields, 0x30 bytes

- m_ID `int`
- m_spellID `int`
- m_overlayFileDataID `int`
- m_screenLocationID `int`
- m_color `int`
- m_scale `float`
- m_iconHighlightSpellClassMask_0 `int`
- m_iconHighlightSpellClassMask_1 `int`
- m_iconHighlightSpellClassMask_2 `int`
- m_iconHighlightSpellClassMask_3 `int`
- m_triggerType `int`
- m_soundEntriesID `int`


# SpellAuraOptions.dbc

0x9 fields, 0x24 bytes

- m_ID `int`
- m_spellID `int`
- m_difficultyID `int`
- m_cumulativeAura `int`
- m_procChance `int`
- m_procCharges `int`
- m_procTypeMask `int`
- m_procCategoryRecovery `int`
- m_spellProcsPerMinuteID `int`


# SpellAuraVisibility.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_spellID `int`
- m_type `int`
- m_flags `int`


# SpellAuraVisXChrSpec.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_spellAuraVisibilityID `int`
- m_chrSpecializationID `int`


# SpellCastingRequirements.dbc

0x7 fields, 0x1c bytes

- m_ID `int`
- m_facingCasterFlags `int`
- m_minFactionID `int`
- m_minReputation `int`
- m_requiredAreasID `int`
- m_requiredAuraVision `int`
- m_requiresSpellFocus `int`


# SpellCastTimes.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_base `int`
- m_perLevel `int`
- m_minimum `int`


# SpellCategories.dbc

0xa fields, 0x28 bytes

- m_ID `int`
- m_spellID `int`
- m_difficultyID `int`
- m_category `int`
- m_defenseType `int`
- m_dispelType `int`
- m_mechanic `int`
- m_preventionType `int`
- m_startRecoveryCategory `int`
- m_chargeCategory `int`


# SpellCategory.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_flags `int`
- m_usesPerWeek `int`
- m_name_lang `string`
- m_maxCharges `int`
- m_chargeRecoveryTime `int`


# SpellCooldowns.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_spellID `int`
- m_difficultyID `int`
- m_categoryRecoveryTime `int`
- m_recoveryTime `int`
- m_startRecoveryTime `int`


# SpellDescriptionVariables.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_variables `string`


# SpellDispelType.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_name_lang `string`
- m_mask `int`
- m_immunityPossible `int`
- m_internalName `string`


# SpellDuration.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_duration `int`
- m_durationPerLevel `int`
- m_maxDuration `int`


# SpellEffect.dbc

0x19 fields, 0x7c bytes

- m_ID `int`
- m_difficultyID `int`
- m_effect `int`
- m_effectAmplitude `float`
- m_effectAura `int`
- m_effectAuraPeriod `int`
- m_effectBasePoints `int`
- m_effectBonusCoefficient `float`
- m_effectChainAmplitude `float`
- m_effectChainTargets `int`
- m_effectDieSides `int`
- m_effectItemType `int`
- m_effectMechanic `int`
- m_effectMiscValue_0 `int`
- m_effectMiscValue_1 `int`
- m_effectPointsPerResource `float`
- m_effectRadiusIndex_0 `int`
- m_effectRadiusIndex_1 `int`
- m_effectRealPointsPerLevel `float`
- m_effectSpellClassMask_0 `int`
- m_effectSpellClassMask_1 `int`
- m_effectSpellClassMask_2 `int`
- m_effectSpellClassMask_3 `int`
- m_effectTriggerSpell `int`
- m_effectPos_facing `float`
- m_implicitTarget_0 `int`
- m_implicitTarget_1 `int`
- m_spellID `int`
- m_effectIndex `int`
- m_effectAttributes `int`
- m_bonusCoefficientFromAP `float`


# SpellEffectScaling.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_coefficient `float`
- m_variance `float`
- m_resourceCoefficient `float`
- m_spellEffectID `int`


# SpellEquippedItems.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_spellID `int`
- m_difficultyID `int`
- m_equippedItemClass `int`
- m_equippedItemInvTypes `int`
- m_equippedItemSubclass `int`


# SpellFlyoutItem.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_spellFlyoutID `int`
- m_spellID `int`
- m_slot `int`


# SpellFlyout.dbc

0x7 fields, 0x1c bytes

- m_ID `int`
- m_flags `int`
- m_raceMask `int`
- m_classMask `int`
- m_spellIconID `int`
- m_name_lang `string`
- m_description_lang `string`


# SpellFocusObject.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_name_lang `string`


# SpellIcon.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_textureFilename `string`


# SpellInterrupts.dbc

0x6 fields, 0x20 bytes

- m_ID `int`
- m_spellID `int`
- m_difficultyID `int`
- m_auraInterruptFlags_0 `int`
- m_auraInterruptFlags_1 `int`
- m_channelInterruptFlags_0 `int`
- m_channelInterruptFlags_1 `int`
- m_interruptFlags `int`


# SpellItemEnchantmentCondition.dbc

0x7 fields, 0x48 bytes

- m_ID `int`
- m_lt_operandType `int`
- m_lt_operand_0 `int`
- m_lt_operand_1 `int`
- m_lt_operand_2 `int`
- m_lt_operand_3 `int`
- m_lt_operand_4 `int`
- m_operator `int`
- m_rt_operandType `int`
- m_rt_operand_0 `int`
- m_rt_operand_1 `int`
- m_rt_operand_2 `int`
- m_rt_operand_3 `int`
- m_rt_operand_4 `int`
- m_logic `int`


# SpellItemEnchantment.dbc

0x12 fields, 0x68 bytes

- m_ID `int`
- m_charges `int`
- m_effect_0 `int`
- m_effect_1 `int`
- m_effect_2 `int`
- m_effectPointsMin_0 `int`
- m_effectPointsMin_1 `int`
- m_effectPointsMin_2 `int`
- m_effectArg_0 `int`
- m_effectArg_1 `int`
- m_effectArg_2 `int`
- m_name_lang `string`
- m_itemVisual `int`
- m_flags `int`
- m_src_itemID `int`
- m_condition_id `int`
- m_requiredSkillID `int`
- m_requiredSkillRank `int`
- m_minLevel `int`
- m_maxLevel `int`
- m_itemLevel `int`
- m_scalingClass `int`
- m_scalingClassRestricted `int`
- m_effectScalingPoints_x `float`
- m_effectScalingPoints_y `float`
- m_effectScalingPoints_z `float`


# SpellKeyboundOverride.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_function `string`


# SpellLearnSpell.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_learnSpellID `int`
- m_overridesSpellID `int`
- m_spellID `int`


# SpellLevels.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_spellID `int`
- m_difficultyID `int`
- m_baseLevel `int`
- m_maxLevel `int`
- m_spellLevel `int`


# SpellMechanic.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_stateName_lang `string`


# SpellMisc.dbc

0xc fields, 0x68 bytes

- m_ID `int`
- m_spellID `int`
- m_difficultyID `int`
- m_attributes_0 `int`
- m_attributes_1 `int`
- m_attributes_2 `int`
- m_attributes_3 `int`
- m_attributes_4 `int`
- m_attributes_5 `int`
- m_attributes_6 `int`
- m_attributes_7 `int`
- m_attributes_8 `int`
- m_attributes_9 `int`
- m_attributes_10 `int`
- m_attributes_11 `int`
- m_attributes_12 `int`
- m_attributes_13 `int`
- m_castingTimeIndex `int`
- m_durationIndex `int`
- m_rangeIndex `int`
- m_speed `float`
- m_spellVisualID_0 `int`
- m_spellVisualID_1 `int`
- m_spellIconID `int`
- m_activeIconID `int`
- m_schoolMask `int`


# SpellProcsPerMinuteMod.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_type `int`
- m_param `int`
- m_coeff `float`
- m_spellProcsPerMinuteID `int`


# SpellProcsPerMinute.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_baseProcRate `float`
- m_flags `int`


# SpellRadius.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_radius `float`
- m_radiusPerLevel `float`
- m_radiusMin `float`
- m_radiusMax `float`


# SpellRange.dbc

0x6 fields, 0x20 bytes

- m_ID `int`
- m_rangeMin_x `float`
- m_rangeMin_y `float`
- m_rangeMax_x `float`
- m_rangeMax_y `float`
- m_flags `int`
- m_displayName_lang `string`
- m_displayNameShort_lang `string`


# Spell.dbc

0x18 fields, 0x60 bytes

- m_ID `int`
- m_name_lang `string`
- m_nameSubtext_lang `string`
- m_description_lang `string`
- m_auraDescription_lang `string`
- m_runeCostID `int`
- m_spellMissileID `int`
- m_descriptionVariablesID `int`
- m_scalingID `int`
- m_auraOptionsID `int`
- m_auraRestrictionsID `int`
- m_castingRequirementsID `int`
- m_categoriesID `int`
- m_classOptionsID `int`
- m_cooldownsID `int`
- m_equippedItemsID `int`
- m_interruptsID `int`
- m_levelsID `int`
- m_reagentsID `int`
- m_shapeshiftID `int`
- m_targetRestrictionsID `int`
- m_totemsID `int`
- m_requiredProjectID `int`
- m_miscID `int`


# SpellRuneCost.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_blood `int`
- m_unholy `int`
- m_frost `int`
- m_chromatic `int`
- m_runicPower `int`


# SpellScaling.dbc

0x9 fields, 0x24 bytes

- m_ID `int`
- m_castTimeMin `int`
- m_castTimeMax `int`
- m_castTimeMaxLevel `int`
- m_class `int`
- m_nerfFactor `float`
- m_nerfMaxLevel `int`
- m_maxScalingLevel `int`
- m_scalesFromItemLevel `int`


# SpellShapeshiftForm.dbc

0xb fields, 0x54 bytes

- m_ID `int`
- m_bonusActionBar `int`
- m_name_lang `string`
- m_flags `int`
- m_creatureType `int`
- m_attackIconID `int`
- m_combatRoundTime `int`
- m_creatureDisplayID_0 `int`
- m_creatureDisplayID_1 `int`
- m_creatureDisplayID_2 `int`
- m_creatureDisplayID_3 `int`
- m_presetSpellID_0 `int`
- m_presetSpellID_1 `int`
- m_presetSpellID_2 `int`
- m_presetSpellID_3 `int`
- m_presetSpellID_4 `int`
- m_presetSpellID_5 `int`
- m_presetSpellID_6 `int`
- m_presetSpellID_7 `int`
- m_mountTypeID `int`
- m_exitSoundEntriesID `int`


# SpellShapeshift.dbc

0x4 fields, 0x18 bytes

- m_ID `int`
- m_shapeshiftExclude_0 `int`
- m_shapeshiftExclude_1 `int`
- m_shapeshiftMask_0 `int`
- m_shapeshiftMask_1 `int`
- m_stanceBarOrder `int`


# SpellSpecialUnitEffect.dbc

0x2 fields, 0x8 bytes

- m_enumID `int`
- m_spellVisualEffectNameID `int`


# SpellTargetRestrictions.dbc

0x9 fields, 0x24 bytes

- m_ID `int`
- m_spellID `int`
- m_difficultyID `int`
- m_coneAngle `float`
- m_width `float`
- m_maxTargets `int`
- m_maxTargetLevel `int`
- m_targetCreatureType `int`
- m_targets `int`


# SpellTotems.dbc

0x3 fields, 0x14 bytes

- m_ID `int`
- m_requiredTotemCategoryID_0 `int`
- m_requiredTotemCategoryID_1 `int`
- m_totem_0 `int`
- m_totem_1 `int`


# Stationery.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_itemID `int`
- m_texture `string`
- m_flags `int`


# StringLookups.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_String `string`


# SummonProperties.dbc

0x6 fields, 0x18 bytes

- m_id `int`
- m_control `int`
- m_faction `int`
- m_title `int`
- m_slot `int`
- m_flags `int`


# Talent.dbc

0xa fields, 0x2c bytes

- m_ID `int`
- m_specID `int`
- m_tierID `int`
- m_columnIndex `int`
- m_spellID `int`
- m_flags `int`
- m_categoryMask_0 `int`
- m_categoryMask_1 `int`
- m_classID `int`
- m_overridesSpellID `int`
- m_description_lang `string`


# TaxiNodes.dbc

0x8 fields, 0x30 bytes

- m_ID `int`
- m_ContinentID `int`
- m_pos_x `float`
- m_pos_y `float`
- m_pos_z `float`
- m_Name_lang `string`
- m_MountCreatureID_0 `int`
- m_MountCreatureID_1 `int`
- m_conditionID `int`
- m_Flags `int`
- m_MapOffset_x `float`
- m_MapOffset_y `float`


# TaxiPathNode.dbc

0x9 fields, 0x2c bytes

- m_ID `int`
- m_PathID `int`
- m_NodeIndex `int`
- m_ContinentID `int`
- m_Loc_x `float`
- m_Loc_y `float`
- m_Loc_z `float`
- m_flags `int`
- m_delay `int`
- m_arrivalEventID `int`
- m_departureEventID `int`


# TaxiPath.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_FromTaxiNode `int`
- m_ToTaxiNode `int`
- m_Cost `int`


# TerrainTypeSounds.dbc

0x1 fields, 0x4 bytes

- m_ID `int`


# TotemCategory.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_name_lang `string`
- m_totemCategoryType `int`
- m_totemCategoryMask `int`


# TradeSkillCategory.dbc

0x6 fields, 0x18 bytes

- m_id `int`
- m_skilllineid `int`
- m_parenttradeskillcategoryid `int`
- m_orderindex `int`
- m_name_lang `string`
- m_flags `int`


# TransportAnimation.dbc

0x5 fields, 0x1c bytes

- m_ID `int`
- m_TransportID `int`
- m_TimeIndex `int`
- m_Pos_x `float`
- m_Pos_y `float`
- m_Pos_z `float`
- m_SequenceID `int`


# TransportPhysics.dbc

0xb fields, 0x2c bytes

- m_ID `int`
- m_waveAmp `float`
- m_waveTimeScale `float`
- m_rollAmp `float`
- m_rollTimeScale `float`
- m_pitchAmp `float`
- m_pitchTimeScale `float`
- m_maxBank `float`
- m_maxBankTurnSpeed `float`
- m_speedDampThresh `float`
- m_speedDamp `float`


# TransportRotation.dbc

0x4 fields, 0x1c bytes

- m_ID `int`
- m_GameObjectsID `int`
- m_TimeIndex `int`
- m_Rot_0 `float`
- m_Rot_1 `float`
- m_Rot_2 `float`
- m_Rot_3 `float`


# UnitBloodLevels.dbc

0x2 fields, 0x10 bytes

- m_ID `int`
- m_Violencelevel_0 `int`
- m_Violencelevel_1 `int`
- m_Violencelevel_2 `int`


# UnitBlood.dbc

0x4 fields, 0x28 bytes

- m_ID `int`
- m_CombatBloodSpurtFront_0 `int`
- m_CombatBloodSpurtFront_1 `int`
- m_CombatBloodSpurtBack_0 `int`
- m_CombatBloodSpurtBack_1 `int`
- m_GroundBlood_0 `string`
- m_GroundBlood_1 `string`
- m_GroundBlood_2 `string`
- m_GroundBlood_3 `string`
- m_GroundBlood_4 `string`


# UnitCondition.dbc

0x5 fields, 0x68 bytes

- m_ID `int`
- m_flags `int`
- m_variable_0 `int`
- m_variable_1 `int`
- m_variable_2 `int`
- m_variable_3 `int`
- m_variable_4 `int`
- m_variable_5 `int`
- m_variable_6 `int`
- m_variable_7 `int`
- m_op_0 `int`
- m_op_1 `int`
- m_op_2 `int`
- m_op_3 `int`
- m_op_4 `int`
- m_op_5 `int`
- m_op_6 `int`
- m_op_7 `int`
- m_value_0 `int`
- m_value_1 `int`
- m_value_2 `int`
- m_value_3 `int`
- m_value_4 `int`
- m_value_5 `int`
- m_value_6 `int`
- m_value_7 `int`


# UnitPowerBar.dbc

0x11 fields, 0x6c bytes

- m_ID `int`
- m_minPower `int`
- m_maxPower `int`
- m_startPower `int`
- m_centerPower `int`
- m_regenerationPeace `float`
- m_regenerationCombat `float`
- m_barType `int`
- m_fileDataID_0 `int`
- m_fileDataID_1 `int`
- m_fileDataID_2 `int`
- m_fileDataID_3 `int`
- m_fileDataID_4 `int`
- m_fileDataID_5 `int`
- m_color_0 `int`
- m_color_1 `int`
- m_color_2 `int`
- m_color_3 `int`
- m_color_4 `int`
- m_color_5 `int`
- m_flags `int`
- m_name_lang `string`
- m_cost_lang `string`
- m_outOfError_lang `string`
- m_toolTip_lang `string`
- m_startInset `float`
- m_endInset `float`


# Vehicle.dbc

0x1e fields, 0xa4 bytes

- m_ID `int`
- m_flags `int`
- m_flagsB `int`
- m_turnSpeed `float`
- m_pitchSpeed `float`
- m_pitchMin `float`
- m_pitchMax `float`
- m_seatID_0 `int`
- m_seatID_1 `int`
- m_seatID_2 `int`
- m_seatID_3 `int`
- m_seatID_4 `int`
- m_seatID_5 `int`
- m_seatID_6 `int`
- m_seatID_7 `int`
- m_mouseLookOffsetPitch `float`
- m_cameraFadeDistScalarMin `float`
- m_cameraFadeDistScalarMax `float`
- m_cameraPitchOffset `float`
- m_facingLimitRight `float`
- m_facingLimitLeft `float`
- m_msslTrgtTurnLingering `float`
- m_msslTrgtPitchLingering `float`
- m_msslTrgtMouseLingering `float`
- m_msslTrgtEndOpacity `float`
- m_msslTrgtArcSpeed `float`
- m_msslTrgtArcRepeat `float`
- m_msslTrgtArcWidth `float`
- m_msslTrgtImpactRadius_x `float`
- m_msslTrgtImpactRadius_y `float`
- m_msslTrgtArcTexture `string`
- m_msslTrgtImpactTexture `string`
- m_msslTrgtImpactModel_0 `string`
- m_msslTrgtImpactModel_1 `string`
- m_cameraYawOffset `float`
- m_uiLocomotionType `int`
- m_msslTrgtImpactTexRadius `float`
- m_vehicleUIIndicatorID `int`
- m_powerDisplayID_0 `int`
- m_powerDisplayID_1 `int`
- m_powerDisplayID_2 `int`


# VehicleSeat.dbc

0x3e fields, 0x108 bytes

- m_ID `int`
- m_flags `int`
- m_attachmentID `int`
- m_attachmentOffset_x `float`
- m_attachmentOffset_y `float`
- m_attachmentOffset_z `float`
- m_enterPreDelay `float`
- m_enterSpeed `float`
- m_enterGravity `float`
- m_enterMinDuration `float`
- m_enterMaxDuration `float`
- m_enterMinArcHeight `float`
- m_enterMaxArcHeight `float`
- m_enterAnimStart `int`
- m_enterAnimLoop `int`
- m_rideAnimStart `int`
- m_rideAnimLoop `int`
- m_rideUpperAnimStart `int`
- m_rideUpperAnimLoop `int`
- m_exitPreDelay `float`
- m_exitSpeed `float`
- m_exitGravity `float`
- m_exitMinDuration `float`
- m_exitMaxDuration `float`
- m_exitMinArcHeight `float`
- m_exitMaxArcHeight `float`
- m_exitAnimStart `int`
- m_exitAnimLoop `int`
- m_exitAnimEnd `int`
- m_passengerYaw `float`
- m_passengerPitch `float`
- m_passengerRoll `float`
- m_passengerAttachmentID `int`
- m_vehicleEnterAnim `int`
- m_vehicleExitAnim `int`
- m_vehicleRideAnimLoop `int`
- m_vehicleEnterAnimBone `int`
- m_vehicleExitAnimBone `int`
- m_vehicleRideAnimLoopBone `int`
- m_vehicleEnterAnimDelay `float`
- m_vehicleExitAnimDelay `float`
- m_vehicleAbilityDisplay `int`
- m_enterUISoundID `int`
- m_exitUISoundID `int`
- m_flagsB `int`
- m_cameraEnteringDelay `float`
- m_cameraEnteringDuration `float`
- m_cameraExitingDelay `float`
- m_cameraExitingDuration `float`
- m_cameraOffset_x `float`
- m_cameraOffset_y `float`
- m_cameraOffset_z `float`
- m_cameraPosChaseRate `float`
- m_cameraFacingChaseRate `float`
- m_cameraEnteringZoom `float`
- m_cameraSeatZoomMin `float`
- m_cameraSeatZoomMax `float`
- m_enterAnimKitID `int`
- m_rideAnimKitID `int`
- m_exitAnimKitID `int`
- m_vehicleEnterAnimKitID `int`
- m_vehicleRideAnimKitID `int`
- m_vehicleExitAnimKitID `int`
- m_cameraModeID `int`
- m_flagsC `int`
- m_uiSkinFileDataID `int`


# VehicleUIIndicator.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_backgroundTexture `string`


# VehicleUIIndSeat.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_vehicleUIIndicatorID `int`
- m_virtualSeatIndex `int`
- m_xPos `float`
- m_yPos `float`


# VocalUISounds.dbc

0x5 fields, 0x1c bytes

- m_ID `int`
- m_vocalUIEnum `int`
- m_raceID `int`
- m_NormalSoundID_0 `int`
- m_NormalSoundID_1 `int`
- m_PissedSoundID_0 `int`
- m_PissedSoundID_1 `int`


# WeaponImpactSounds.dbc

0x5 fields, 0x5c bytes

- m_ID `int`
- m_WeaponSubClassID `int`
- m_ParrySoundType `int`
- m_impactSoundID_0 `int`
- m_impactSoundID_1 `int`
- m_impactSoundID_2 `int`
- m_impactSoundID_3 `int`
- m_impactSoundID_4 `int`
- m_impactSoundID_5 `int`
- m_impactSoundID_6 `int`
- m_impactSoundID_7 `int`
- m_impactSoundID_8 `int`
- m_impactSoundID_9 `int`
- m_critImpactSoundID_0 `int`
- m_critImpactSoundID_1 `int`
- m_critImpactSoundID_2 `int`
- m_critImpactSoundID_3 `int`
- m_critImpactSoundID_4 `int`
- m_critImpactSoundID_5 `int`
- m_critImpactSoundID_6 `int`
- m_critImpactSoundID_7 `int`
- m_critImpactSoundID_8 `int`
- m_critImpactSoundID_9 `int`


# WeaponSwingSounds2.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_SwingType `int`
- m_Crit `int`
- m_SoundID `int`


# World_PVP_Area.dbc

0x7 fields, 0x1c bytes

- m_ID `int`
- m_area_ID `int`
- m_next_time_worldstate `int`
- m_game_time_worldstate `int`
- m_battle_populate_time `int`
- m_min_level `int`
- m_max_level `int`


# WorldChunkSounds.dbc

0x6 fields, 0x1c bytes

- m_MapID `int`
- m_ChunkX `int`
- m_ChunkY `int`
- m_SubchunkX `int`
- m_SubchunkY `int`
- m_SoundOverrideID `int`


# WorldEffect.dbc

0x7 fields, 0x1c bytes

- m_ID `int`
- m_targetType `int`
- m_targetAsset `int`
- m_questFeedbackEffectID `int`
- m_playerConditionID `int`
- m_combatConditionID `int`
- m_whenToDisplay `int`


# WorldElapsedTimer.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_name_lang `string`
- m_flags `int`
- m_type `int`


# WorldMapArea.dbc

0xe fields, 0x38 bytes

- m_ID `int`
- m_mapID `int`
- m_areaID `int`
- m_areaName `string`
- m_locLeft `float`
- m_locRight `float`
- m_locTop `float`
- m_locBottom `float`
- m_displayMapID `int`
- m_defaultDungeonFloor `int`
- m_parentWorldMapID `int`
- m_flags `int`
- m_levelRangeMin `int`
- m_levelRangeMax `int`


# WorldMapContinent.dbc

0xb fields, 0x38 bytes

- m_ID `int`
- m_mapID `int`
- m_leftBoundary `int`
- m_rightBoundary `int`
- m_topBoundary `int`
- m_bottomBoundary `int`
- m_continentOffset_x `float`
- m_continentOffset_y `float`
- m_scale `float`
- m_taxiMin_x `float`
- m_taxiMin_y `float`
- m_taxiMax_x `float`
- m_taxiMax_y `float`
- m_worldMapID `int`


# WorldMapOverlay.dbc

0xd fields, 0x40 bytes

- m_ID `int`
- m_mapAreaID `int`
- m_areaID_0 `int`
- m_areaID_1 `int`
- m_areaID_2 `int`
- m_areaID_3 `int`
- m_textureName `string`
- m_textureWidth `int`
- m_textureHeight `int`
- m_offsetX `int`
- m_offsetY `int`
- m_hitRectTop `int`
- m_hitRectLeft `int`
- m_hitRectBottom `int`
- m_hitRectRight `int`
- m_playerConditionID `int`


# WorldMapTransforms.dbc

0xa fields, 0x3c bytes

- m_ID `int`
- m_mapID `int`
- m_regionMin_x `float`
- m_regionMin_y `float`
- m_regionMin_z `float`
- m_regionMax_x `float`
- m_regionMax_y `float`
- m_regionMax_z `float`
- m_newMapID `int`
- m_regionOffset_x `float`
- m_regionOffset_y `float`
- m_newDungeonMapID `int`
- m_flags `int`
- m_newAreaID `int`
- m_regionScale `float`


# WorldSafeLocs.dbc

0x5 fields, 0x1c bytes

- m_ID `int`
- m_continent `int`
- m_loc_x `float`
- m_loc_y `float`
- m_loc_z `float`
- m_facing `float`
- m_areaName_lang `string`


# WorldStateExpression.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_expression `string`


# WorldState.dbc

0x1 fields, 0x4 bytes

- m_ID `int`


# WorldStateUI.dbc

0xf fields, 0x44 bytes

- m_ID `int`
- m_mapID `int`
- m_areaID `int`
- m_phaseUseFlags `int`
- m_phaseID `int`
- m_phaseGroupID `int`
- m_icon `string`
- m_string_lang `string`
- m_tooltip_lang `string`
- m_stateVariable `int`
- m_type `int`
- m_dynamicIcon `string`
- m_dynamicTooltip_lang `string`
- m_extendedUI `string`
- m_extendedUIStateVariable_0 `int`
- m_extendedUIStateVariable_1 `int`
- m_extendedUIStateVariable_2 `int`


# WorldStateZoneSounds.dbc

0x8 fields, 0x24 bytes

- m_WorldStateID `int`
- m_WorldStateValue `int`
- m_AreaID `int`
- m_WMOAreaID `int`
- m_ZoneIntroMusicID `int`
- m_ZoneMusicID `int`
- m_SoundAmbienceID `int`
- m_SoundProviderPreferencesID `int`


# ZoneIntroMusicTable.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_Name `string`
- m_SoundID `int`
- m_Priority `int`
- m_MinDelayMinutes `int`


# ZoneMusic.dbc

0x5 fields, 0x20 bytes

- m_ID `int`
- m_SetName `string`
- m_SilenceIntervalMin_0 `int`
- m_SilenceIntervalMin_1 `int`
- m_SilenceIntervalMax_0 `int`
- m_SilenceIntervalMax_1 `int`
- m_Sounds_0 `int`
- m_Sounds_1 `int`


# AnimationData.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_Name `string`
- m_Flags `int`
- m_Fallback `int`
- m_BehaviorID `int`
- m_BehaviorTier `int`


# AreaTable.dbc

0x1b fields, 0x7c bytes

- m_ID `int`
- m_ContinentID `int`
- m_ParentAreaID `int`
- m_AreaBit `int`
- m_flags_0 `int`
- m_flags_1 `int`
- m_SoundProviderPref `int`
- m_SoundProviderPrefUnderwater `int`
- m_AmbienceID `int`
- m_ZoneMusic `int`
- m_ZoneName `string`
- m_IntroSound `int`
- m_ExplorationLevel `int`
- m_AreaName_lang `string`
- m_factionGroupMask `int`
- m_liquidTypeID_0 `int`
- m_liquidTypeID_1 `int`
- m_liquidTypeID_2 `int`
- m_liquidTypeID_3 `int`
- m_minElevation `float`
- m_ambient_multiplier `float`
- m_lightid `int`
- m_mountFlags `int`
- m_uwIntroSound `int`
- m_uwZoneMusic `int`
- m_uwAmbience `int`
- m_world_pvp_id `int`
- m_pvpCombatWorldStateID `int`
- m_wildBattlePetLevelMin `int`
- m_wildBattlePetLevelMax `int`
- m_windSettingsID `int`


# FileData.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_filename `string`
- m_filepath `string`


# FootprintTextures.dbc

0x2 fields, 0x8 bytes

- m_ID `int`
- m_FootstepFilename `string`


# GroundEffectDoodad.dbc

0x5 fields, 0x14 bytes

- m_ID `int`
- m_doodadpath `string`
- m_flags `int`
- m_animscale `float`
- m_pushscale `float`


# LightData.dbc

0x19 fields, 0x64 bytes

- m_ID `int`
- m_lightParamID `int`
- m_time `int`
- m_directColor `int`
- m_ambientColor `int`
- m_skyTopColor `int`
- m_skyMiddleColor `int`
- m_skyBand1Color `int`
- m_skyBand2Color `int`
- m_skySmogColor `int`
- m_skyFogColor `int`
- m_sunColor `int`
- m_cloudSunColor `int`
- m_cloudEmissiveColor `int`
- m_cloudLayer1AmbientColor `int`
- m_cloudLayer2AmbientColor `int`
- m_oceanCloseColor `int`
- m_oceanFarColor `int`
- m_riverCloseColor `int`
- m_riverFarColor `int`
- m_shadowOpacity `int`
- m_fogEnd `float`
- m_fogScaler `float`
- m_cloudDensity `float`
- m_fogDensity `float`


# LightParams.dbc

0xa fields, 0x28 bytes

- m_ID `int`
- m_highlightSky `int`
- m_lightSkyboxID `int`
- m_cloudTypeID `int`
- m_glow `float`
- m_waterShallowAlpha `float`
- m_waterDeepAlpha `float`
- m_oceanShallowAlpha `float`
- m_oceanDeepAlpha `float`
- m_flags `int`


# Light.dbc

0x8 fields, 0x3c bytes

- m_ID `int`
- m_continentID `int`
- m_x `float`
- m_y `float`
- m_z `float`
- m_falloffStart `float`
- m_falloffEnd `float`
- m_lightParamsID_0 `int`
- m_lightParamsID_1 `int`
- m_lightParamsID_2 `int`
- m_lightParamsID_3 `int`
- m_lightParamsID_4 `int`
- m_lightParamsID_5 `int`
- m_lightParamsID_6 `int`
- m_lightParamsID_7 `int`


# LightSkybox.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_name `string`
- m_flags `int`


# LiquidMaterial.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_LVF `int`
- m_flags `int`


# LiquidObject.dbc

0x6 fields, 0x18 bytes

- m_ID `int`
- m_flowDirection `float`
- m_flowSpeed `float`
- m_liquidTypeID `int`
- m_fishable `int`
- m_reflection `int`


# LiquidType.dbc

0x13 fields, 0xb4 bytes

- m_ID `int`
- m_name `string`
- m_flags `int`
- m_soundBank `int`
- m_soundID `int`
- m_spellID `int`
- m_maxDarkenDepth `float`
- m_fogDarkenIntensity `float`
- m_ambDarkenIntensity `float`
- m_dirDarkenIntensity `float`
- m_lightID `int`
- m_particleScale `float`
- m_particleMovement `int`
- m_particleTexSlots `int`
- m_materialID `int`
- m_texture_0 `string`
- m_texture_1 `string`
- m_texture_2 `string`
- m_texture_3 `string`
- m_texture_4 `string`
- m_texture_5 `string`
- m_color_0 `int`
- m_color_1 `int`
- m_float_0 `float`
- m_float_1 `float`
- m_float_2 `float`
- m_float_3 `float`
- m_float_4 `float`
- m_float_5 `float`
- m_float_6 `float`
- m_float_7 `float`
- m_float_8 `float`
- m_float_9 `float`
- m_float_10 `float`
- m_float_11 `float`
- m_float_12 `float`
- m_float_13 `float`
- m_float_14 `float`
- m_float_15 `float`
- m_float_16 `float`
- m_float_17 `float`
- m_int_0 `int`
- m_int_1 `int`
- m_int_2 `int`
- m_int_3 `int`


# Map.dbc

0x14 fields, 0x54 bytes

- m_ID `int`
- m_Directory `string`
- m_InstanceType `int`
- m_Flags `int`
- m_MapType `int`
- m_MapName_lang `string`
- m_areaTableID `int`
- m_MapDescription0_lang `string`
- m_MapDescription1_lang `string`
- m_LoadingScreenID `int`
- m_minimapIconScale `float`
- m_corpseMapID `int`
- m_corpse_x `float`
- m_corpse_y `float`
- m_timeOfDayOverride `int`
- m_expansionID `int`
- m_raidOffset `int`
- m_maxPlayers `int`
- m_parentMapID `int`
- m_cosmeticParentMapID `int`
- m_timeOffset `int`


# SoundBusName.dbc

0x2 fields, 0x8 bytes

- m_EnumID `int`
- m_Name `string`


# SoundBus.dbc

0xb fields, 0x2c bytes

- m_ID `int`
- m_Parent `int`
- m_DefaultPriority `int`
- m_DefaultPriorityPenalty `int`
- m_RaidPriority `int`
- m_RaidPriorityPenalty `int`
- m_DefaultVolume `float`
- m_RaidVolume `float`
- m_DefaultPlaybackLimit `int`
- m_RaidPlaybackLimit `int`
- m_BusEnumID `int`


# SoundEmitterPillPoints.dbc

0x3 fields, 0x14 bytes

- m_ID `int`
- m_soundEmittersID `int`
- m_position_x `float`
- m_position_y `float`
- m_position_z `float`


# SoundEmitters.dbc

0xc fields, 0x40 bytes

- m_ID `int`
- m_position_x `float`
- m_position_y `float`
- m_position_z `float`
- m_direction_x `float`
- m_direction_y `float`
- m_direction_z `float`
- m_soundEntriesID `int`
- m_mapID `int`
- m_name `string`
- m_emitterType `int`
- m_PhaseID `int`
- m_PhaseGroupID `int`
- m_PhaseUseFlags `int`
- m_flags `int`
- m_worldStateExpressionID `int`


# SoundEntriesAdvanced.dbc

0x1d fields, 0xc0 bytes

- m_ID `int`
- m_soundEntryID `int`
- m_innerRadius2D `float`
- m_timeA `int`
- m_timeB `int`
- m_timeC `int`
- m_timeD `int`
- m_randomOffsetRange `int`
- m_usage `int`
- m_timeIntervalMin `int`
- m_timeIntervalMax `int`
- m_volumeSliderCategory `int`
- m_duckToSFX `float`
- m_duckToMusic `float`
- m_duckToAmbience `float`
- m_innerRadiusOfInfluence `float`
- m_outerRadiusOfInfluence `float`
- m_timeToDuck `int`
- m_timeToUnduck `int`
- m_insideAngle `float`
- m_outsideAngle `float`
- m_outsideVolume `float`
- m_outerRadius2D `float`
- m_minRandomPosOffset `int`
- m_maxRandomPosOffset `int`
- m_duckToDialog `float`
- m_duckToSuppressors `float`
- m_msOffset `int`
- m_volume_0 `float`
- m_volume_1 `float`
- m_volume_2 `float`
- m_volume_3 `float`
- m_volume_4 `float`
- m_volume_5 `float`
- m_volume_6 `float`
- m_volume_7 `float`
- m_volume_8 `float`
- m_volume_9 `float`
- m_volume_10 `float`
- m_volume_11 `float`
- m_volume_12 `float`
- m_volume_13 `float`
- m_volume_14 `float`
- m_volume_15 `float`
- m_volume_16 `float`
- m_volume_17 `float`
- m_volume_18 `float`
- m_volume_19 `float`


# SoundEntriesFallbacks.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_soundEntriesID `int`
- m_fallbackSoundEntriesID `int`


# SoundEntries.dbc

0x12 fields, 0xe0 bytes

- m_ID `int`
- m_soundType `int`
- m_name `string`
- m_FileDataID_0 `int`
- m_FileDataID_1 `int`
- m_FileDataID_2 `int`
- m_FileDataID_3 `int`
- m_FileDataID_4 `int`
- m_FileDataID_5 `int`
- m_FileDataID_6 `int`
- m_FileDataID_7 `int`
- m_FileDataID_8 `int`
- m_FileDataID_9 `int`
- m_FileDataID_10 `int`
- m_FileDataID_11 `int`
- m_FileDataID_12 `int`
- m_FileDataID_13 `int`
- m_FileDataID_14 `int`
- m_FileDataID_15 `int`
- m_FileDataID_16 `int`
- m_FileDataID_17 `int`
- m_FileDataID_18 `int`
- m_FileDataID_19 `int`
- m_Freq_0 `int`
- m_Freq_1 `int`
- m_Freq_2 `int`
- m_Freq_3 `int`
- m_Freq_4 `int`
- m_Freq_5 `int`
- m_Freq_6 `int`
- m_Freq_7 `int`
- m_Freq_8 `int`
- m_Freq_9 `int`
- m_Freq_10 `int`
- m_Freq_11 `int`
- m_Freq_12 `int`
- m_Freq_13 `int`
- m_Freq_14 `int`
- m_Freq_15 `int`
- m_Freq_16 `int`
- m_Freq_17 `int`
- m_Freq_18 `int`
- m_Freq_19 `int`
- m_volumeFloat `float`
- m_flags `int`
- m_minDistance `float`
- m_distanceCutoff `float`
- m_EAXDef `int`
- m_soundEntriesAdvancedID `int`
- m_volumevariationplus `float`
- m_volumevariationminus `float`
- m_pitchvariationplus `float`
- m_pitchvariationminus `float`
- m_pitchAdjust `float`
- m_dialogtype `int`
- m_busOverwriteID `int`


# SpellChainEffects.dbc

0x30 fields, 0xdc bytes

- m_ID `int`
- m_AvgSegLen `float`
- m_Width `float`
- m_NoiseScale `float`
- m_TexCoordScale `float`
- m_SegDuration `int`
- m_SegDelay `int`
- m_Flags `int`
- m_JointCount `int`
- m_JointOffsetRadius `float`
- m_JointsPerMinorJoint `int`
- m_MinorJointsPerMajorJoint `int`
- m_MinorJointScale `float`
- m_MajorJointScale `float`
- m_JointMoveSpeed `float`
- m_JointSmoothness `float`
- m_MinDurationBetweenJointJumps `float`
- m_MaxDurationBetweenJointJumps `float`
- m_WaveHeight `float`
- m_WaveFreq `float`
- m_WaveSpeed `float`
- m_MinWaveAngle `float`
- m_MaxWaveAngle `float`
- m_MinWaveSpin `float`
- m_MaxWaveSpin `float`
- m_ArcHeight `float`
- m_MinArcAngle `float`
- m_MaxArcAngle `float`
- m_MinArcSpin `float`
- m_MaxArcSpin `float`
- m_DelayBetweenEffects `float`
- m_MinFlickerOnDuration `float`
- m_MaxFlickerOnDuration `float`
- m_MinFlickerOffDuration `float`
- m_MaxFlickerOffDuration `float`
- m_PulseSpeed `float`
- m_PulseOnLength `float`
- m_PulseFadeLength `float`
- m_Alpha `int`
- m_Red `int`
- m_Green `int`
- m_Blue `int`
- m_BlendMode `int`
- m_RenderLayer `int`
- m_TextureLength `float`
- m_WavePhase `float`
- m_SpellChainEffectID_0 `int`
- m_SpellChainEffectID_1 `int`
- m_SpellChainEffectID_2 `int`
- m_SpellChainEffectID_3 `int`
- m_SpellChainEffectID_4 `int`
- m_SpellChainEffectID_5 `int`
- m_SpellChainEffectID_6 `int`
- m_SpellChainEffectID_7 `int`
- m_SpellChainEffectID_8 `int`
- m_SpellChainEffectID_9 `int`
- m_SpellChainEffectID_10 `int`
- m_Texture `string`


# Startup_Strings.dbc

0x3 fields, 0xc bytes

- m_ID `int`
- m_name `string`
- m_message_lang `string`


# TerrainMaterial.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_name `string`
- m_shader `int`
- m_envMapPath `string`


# TerrainType.dbc

0x6 fields, 0x1c bytes

- m_TerrainID `int`
- m_TerrainDesc `string`
- m_FootstepSprayRun `int`
- m_FootstepSprayWalk `int`
- m_SoundID `int`
- m_Flags `int`


# VideoHardware.dbc

0x17 fields, 0x5c bytes

- m_ID `int`
- m_vendorID `int`
- m_deviceID `int`
- m_farclipIdx `int`
- m_terrainLODDistIdx `int`
- m_terrainShadowLOD `int`
- m_detailDoodadDensityIdx `int`
- m_detailDoodadAlpha `int`
- m_animatingDoodadIdx `int`
- m_trilinear `int`
- m_numLights `int`
- m_specularity `int`
- m_waterLODIdx `int`
- m_particleDensityIdx `int`
- m_unitDrawDistIdx `int`
- m_smallCullDistIdx `int`
- m_resolutionIdx `int`
- m_baseMipLevel `int`
- m_oglOverrides `string`
- m_d3dOverrides `string`
- m_fixLag `int`
- m_multisample `int`
- m_atlasdisable `int`


# Weather.dbc

0xa fields, 0x34 bytes

- m_ID `int`
- m_ambienceID `int`
- m_type `int`
- m_effectType `int`
- m_intensity_x `float`
- m_intensity_y `float`
- m_transitionSkyBox `float`
- m_effectColor_r `float`
- m_effectColor_g `float`
- m_effectColor_b `float`
- m_effectTexture `string`
- m_soundAmbienceID `int`
- m_windSettingsID `int`


# WMOAreaTable.dbc

0xf fields, 0x3c bytes

- m_ID `int`
- m_WMOID `int`
- m_NameSetID `int`
- m_WMOGroupID `int`
- m_SoundProviderPref `int`
- m_SoundProviderPrefUnderwater `int`
- m_AmbienceID `int`
- m_ZoneMusic `int`
- m_IntroSound `int`
- m_flags `int`
- m_AreaTableID `int`
- m_AreaName_lang `string`
- m_uwIntroSound `int`
- m_uwZoneMusic `int`
- m_uwAmbience `int`


# ZoneLightPoint.dbc

0x4 fields, 0x14 bytes

- m_ID `int`
- m_zoneLightID `int`
- m_pos_x `float`
- m_pos_y `float`
- m_pointOrder `int`


# ZoneLight.dbc

0x4 fields, 0x10 bytes

- m_ID `int`
- m_name `string`
- m_mapID `int`
- m_lightID `int`
