export const ACTIONS = Object.freeze({
  APPROVE_SELLER: 'approve_seller',
  MANAGE_SELLER_USERS: 'manage_seller_users',
  MANAGE_DONOR_ASSETS: 'manage_donor_assets',
  CREATE_PART: 'create_part',
  DELETE_PART: 'delete_part',
  ASSIGN_LOCATION: 'assign_location',
  MANAGE_LOCATIONS: 'manage_locations',
  CREATE_WORKER_TASK: 'create_worker_task',
  COMPLETE_WORKER_TASK: 'complete_worker_task',
  EDIT_PRICE: 'edit_price',
  MARK_PRICE_READY: 'mark_price_ready',
  CREATE_RESERVATION: 'create_reservation',
  CONVERT_RESERVATION_TO_ORDER: 'convert_reservation_to_order',
  UPDATE_PAYMENT_STATUS: 'update_payment_status',
  UPDATE_SHIPMENT_STATUS: 'update_shipment_status',
  VIEW_AUDIT_LOGS: 'view_audit_logs',
  VIEW_DASHBOARD: 'view_dashboard',
  EDIT_TAX_PROFILE: 'edit_tax_profile'
});

export const ROLES = Object.freeze({
  PLATFORM_ADMIN: 'platform_admin',
  SELLER_ADMIN: 'seller_admin',
  WAREHOUSE_MANAGER: 'warehouse_manager',
  WAREHOUSE_WORKER: 'warehouse_worker',
  PRICING_MANAGER: 'pricing_manager',
  SALES_OPERATOR: 'sales_operator',
  READ_ONLY_AUDITOR: 'read_only_auditor'
});

export const ROLE_PERMISSIONS = Object.freeze({
  [ROLES.PLATFORM_ADMIN]: new Set([
    ACTIONS.APPROVE_SELLER,
    ACTIONS.VIEW_AUDIT_LOGS,
    ACTIONS.VIEW_DASHBOARD
  ]),

  [ROLES.SELLER_ADMIN]: new Set([
    ACTIONS.MANAGE_SELLER_USERS,
    ACTIONS.MANAGE_DONOR_ASSETS,
    ACTIONS.CREATE_PART,
    ACTIONS.DELETE_PART,
    ACTIONS.ASSIGN_LOCATION,
    ACTIONS.MANAGE_LOCATIONS,
    ACTIONS.CREATE_WORKER_TASK,
    ACTIONS.COMPLETE_WORKER_TASK,
    ACTIONS.EDIT_PRICE,
    ACTIONS.MARK_PRICE_READY,
    ACTIONS.CREATE_RESERVATION,
    ACTIONS.CONVERT_RESERVATION_TO_ORDER,
    ACTIONS.UPDATE_PAYMENT_STATUS,
    ACTIONS.UPDATE_SHIPMENT_STATUS,
    ACTIONS.VIEW_AUDIT_LOGS,
    ACTIONS.VIEW_DASHBOARD,
    ACTIONS.EDIT_TAX_PROFILE
  ]),

  [ROLES.WAREHOUSE_MANAGER]: new Set([
    ACTIONS.CREATE_PART,
    ACTIONS.ASSIGN_LOCATION,
    ACTIONS.MANAGE_LOCATIONS,
    ACTIONS.CREATE_WORKER_TASK,
    ACTIONS.COMPLETE_WORKER_TASK,
    ACTIONS.UPDATE_SHIPMENT_STATUS,
    ACTIONS.VIEW_DASHBOARD
  ]),

  [ROLES.WAREHOUSE_WORKER]: new Set([
    ACTIONS.COMPLETE_WORKER_TASK,
    ACTIONS.VIEW_DASHBOARD
  ]),

  [ROLES.PRICING_MANAGER]: new Set([
    ACTIONS.EDIT_PRICE,
    ACTIONS.MARK_PRICE_READY,
    ACTIONS.VIEW_DASHBOARD
  ]),

  [ROLES.SALES_OPERATOR]: new Set([
    ACTIONS.CREATE_RESERVATION,
    ACTIONS.CONVERT_RESERVATION_TO_ORDER,
    ACTIONS.UPDATE_PAYMENT_STATUS,
    ACTIONS.VIEW_DASHBOARD
  ]),

  [ROLES.READ_ONLY_AUDITOR]: new Set([
    ACTIONS.VIEW_AUDIT_LOGS,
    ACTIONS.VIEW_DASHBOARD
  ])
});

export const MUTATING_ACTIONS = new Set([
  ACTIONS.APPROVE_SELLER,
  ACTIONS.MANAGE_SELLER_USERS,
  ACTIONS.MANAGE_DONOR_ASSETS,
  ACTIONS.CREATE_PART,
  ACTIONS.DELETE_PART,
  ACTIONS.ASSIGN_LOCATION,
  ACTIONS.MANAGE_LOCATIONS,
  ACTIONS.CREATE_WORKER_TASK,
  ACTIONS.COMPLETE_WORKER_TASK,
  ACTIONS.EDIT_PRICE,
  ACTIONS.MARK_PRICE_READY,
  ACTIONS.CREATE_RESERVATION,
  ACTIONS.CONVERT_RESERVATION_TO_ORDER,
  ACTIONS.UPDATE_PAYMENT_STATUS,
  ACTIONS.UPDATE_SHIPMENT_STATUS,
  ACTIONS.EDIT_TAX_PROFILE
]);

export const AUDIT_REQUIRED_ACTIONS = new Set([
  ACTIONS.APPROVE_SELLER,
  ACTIONS.CREATE_PART,
  ACTIONS.DELETE_PART,
  ACTIONS.ASSIGN_LOCATION,
  ACTIONS.EDIT_PRICE,
  ACTIONS.MARK_PRICE_READY,
  ACTIONS.CREATE_RESERVATION,
  ACTIONS.CONVERT_RESERVATION_TO_ORDER,
  ACTIONS.UPDATE_PAYMENT_STATUS,
  ACTIONS.UPDATE_SHIPMENT_STATUS,
  ACTIONS.EDIT_TAX_PROFILE
]);

export function normalizeRole(role) {
  if (!role || typeof role !== 'string') return null;
  return role.trim().toLowerCase();
}

export function can(role, action) {
  const normalizedRole = normalizeRole(role);
  if (!normalizedRole || !action) return false;
  const permissions = ROLE_PERMISSIONS[normalizedRole];
  return Boolean(permissions && permissions.has(action));
}

export function isMutatingAction(action) {
  return MUTATING_ACTIONS.has(action);
}

export function requiresAudit(action) {
  return AUDIT_REQUIRED_ACTIONS.has(action);
}

export function permissionDecision({ role, action, userSellerId, entitySellerId }) {
  const normalizedRole = normalizeRole(role);

  if (!normalizedRole) {
    return { allowed: false, reason: 'unauthenticated' };
  }

  if (!can(normalizedRole, action)) {
    return { allowed: false, reason: 'role_not_allowed' };
  }

  if (normalizedRole !== ROLES.PLATFORM_ADMIN && entitySellerId && userSellerId && entitySellerId !== userSellerId) {
    return { allowed: false, reason: 'tenant_mismatch' };
  }

  return {
    allowed: true,
    reason: 'allowed',
    audit_required: requiresAudit(action),
    mutating: isMutatingAction(action)
  };
}
