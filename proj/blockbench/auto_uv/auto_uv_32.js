(function() {
    var autoUV32Action;

    BBPlugin.register('auto_uv_32', {
        title: '自动UV32',
        author: 'Ringozia',
        description: '适用于尺寸32*32贴图的自动UV，基岩版逐面UV专用',
        icon: 'border_inner',
        version: '3.0.0',
        variant: 'both',
        onload() {
            autoUV32Action = new Action('auto_uv_32_btn', {
                name: '自动UV(32*32贴图适用)',
                description: '32×适用*为该块所有面更新UV',
                icon: 'border_inner', // 图标样式
                category: 'edit',
                click: function () {
                    // 0. 安全检查：必须是基岩版或标准模型
                    if (Project.box_uv) {
                        Blockbench.showMessage('错误：此插件仅支持“逐面 UV (Per-face UV)”。\n当前项目使用的是“箱型 UV (Box UV)”，无法单独调整面的 UV 大小。', 'center');
                        return;
                    }

                    // 1. 检查选中方块
                    if (Cube.selected.length === 0) {
                        Blockbench.showQuickMessage('请先选择一个方块！');
                        return;
                    }

                    // 2. 初始化撤销
                    Undo.initEdit({elements: Cube.selected, uv_only: true});

                    // 3. 确定目标面
                    // Blockbench 逻辑：如果 main_uv.face 有值，说明用户刚才点击了特定面
                    // 如果 main_uv.face 为 null 或 undefined，说明用户可能刚选了方块但没选面
                    let targetFace = (typeof main_uv !== 'undefined' && main_uv.face) ? main_uv.face : null;
                    
                    let updateCount = 0;

                    Cube.selected.forEach(cube => {
                        let size = cube.size(); // [x, y, z]

                        // 遍历所有可能的面
                        ['north', 'south', 'east', 'west', 'up', 'down'].forEach(faceKey => {
                            // 关键筛选：如果有特定选中的面，就跳过其他面；如果没有，就处理所有面。
                            if (targetFace && faceKey !== targetFace) return;

                            let face = cube.faces[faceKey];
                            // 检查面是否有贴图，如果没有贴图，UV通常是无效的，跳过
                            if (!face || face.texture === null && cube.faces[faceKey].enabled !== false) {
                                // 注意：即使没有贴图，只要面是启用的，我们也应该尝试计算UV，
                                // 因为用户可能稍后会贴图。
                            }

                            // 计算 3D 尺寸
                            let dim = getDimensions(faceKey, size);
                            
                            // === 核心功能：尺寸 * 0.5 ===
                            let targetW = dim.w * 0.5;
                            let targetH = dim.h * 0.5;

                            // 修改 UV (基岩版格式: [u1, v1, u2, v2])
                            // 保持左上角 u1, v1 不变
                            let u1 = face.uv[0];
                            let v1 = face.uv[1];
                            
                            face.uv[2] = u1 + targetW;
                            face.uv[3] = v1 + targetH;

                            updateCount++;
                        });
                    });

                    // 4. 提交更改
                    if (updateCount > 0) {
                        Undo.finishEdit('应用自动 UV 32');
                        
                        // 强制刷新 3D 视图
                        Canvas.updateView({elements: Cube.selected});
                        
                        // 强制刷新 UV 窗口 (尝试多种刷新方法)
                        if (typeof main_uv !== 'undefined') {
                            if (main_uv.loadData) main_uv.loadData();
                            if (main_uv.update) main_uv.update();
                        }
                        
                        Blockbench.showQuickMessage(`成功：已缩放 ${updateCount} 个面的 UV`, 2000);
                    } else {
                        // 如果没有面被更新（可能是没选中面，或者面被隐藏了）
                        Blockbench.showQuickMessage('未检测到有效面，请在UV编辑器中选中一个面再试。');
                    }
                }
            });

            // 添加到菜单栏 (Filter 菜单)
            MenuBar.addAction(autoUV32Action, 'filter');
            
            // 添加到 UV 编辑器工具栏
            if (typeof Toolbars !== 'undefined' && Toolbars.uv_dialog) {
                Toolbars.uv_dialog.add(autoUV32Action);
            }
        },
        onunload() {
            autoUV32Action.delete();
        }
    });

    // 辅助函数：获取面的 3D 宽高
    function getDimensions(face, size) {
        let w = 0, h = 0;
        switch(face) {
            case 'north': 
            case 'south': 
                w = size[0]; h = size[1]; break; // X, Y
            case 'east': 
            case 'west': 
                w = size[2]; h = size[1]; break; // Z, Y
            case 'up': 
            case 'down': 
                w = size[0]; h = size[2]; break; // X, Z
        }
        return {w, h};
    }

})();