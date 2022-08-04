from explorer_s_common.consts import ERROR_DICT

ERROR_DICT.update({
    13000: '找不对对象',
    13001: '无效的app_id',
    13004: '操作失败，请重试',
})

# 权限
PERMESSIONS = [
    # 用户管理
    {'code': 'dashboard_manage', 'name': 'dashboard管理', 'parent': None},
    {'code': 'query_dashboard', 'name': '查询dashboard', 'parent': 'dashboard_manage'},

,

    # 用户管理
    {'code': 'user_manage', 'name': '用户管理', 'parent': None},
    {'code': 'query_user', 'name': '查询用户', 'parent': 'user_manage'},




# 角色权限
ROLE_PERMESSIONS = {
    # 普通购买者
    'role_buyer': [
        'fil_recharge', 'fil_withdraw', 'query_machine_asset', 'query_user', 'query_miner',
        'query_miner_model', 'query_miner_product', 'query_software_order', 'query_hardware_order',
        'query_wallet_address', 'query_dashboard'
    ],
    # 新闻运营
    'role_reporter': [
        'query_notice', 'add_notice', 'modify_notice', 'remove_notice'
    ]
}
