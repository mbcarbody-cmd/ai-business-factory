import { ACTIONS, ROLES, can, permissionDecision } from '../src/auth/permissions.js';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function deny(role, action, message) {
  assert(!can(role, action), message);
}

function allow(role, action, message) {
  assert(can(role, action), message);
}

function run() {
  allow(ROLES.SELLER_ADMIN, ACTIONS.CREATE_PART, 'seller_admin must create parts');
  allow(ROLES.SELLER_ADMIN, ACTIONS.CONVERT_RESERVATION_TO_ORDER, 'seller_admin must convert reservation to order');
  allow(ROLES.SELLER_ADMIN, ACTIONS.EDIT_TAX_PROFILE, 'seller_admin must edit tax profile');

  allow(ROLES.WAREHOUSE_MANAGER, ACTIONS.ASSIGN_LOCATION, 'warehouse_manager must assign locations');
  allow(ROLES.WAREHOUSE_MANAGER, ACTIONS.CREATE_WORKER_TASK, 'warehouse_manager must create worker tasks');
  deny(ROLES.WAREHOUSE_MANAGER, ACTIONS.EDIT_TAX_PROFILE, 'warehouse_manager must not edit tax profile');
  deny(ROLES.WAREHOUSE_MANAGER, ACTIONS.APPROVE_SELLER, 'warehouse_manager must not approve sellers');

  allow(ROLES.WAREHOUSE_WORKER, ACTIONS.COMPLETE_WORKER_TASK, 'warehouse_worker must complete assigned tasks');
  deny(ROLES.WAREHOUSE_WORKER, ACTIONS.EDIT_PRICE, 'warehouse_worker must not edit price');
  deny(ROLES.WAREHOUSE_WORKER, ACTIONS.CONVERT_RESERVATION_TO_ORDER, 'warehouse_worker must not create orders');
  deny(ROLES.WAREHOUSE_WORKER, ACTIONS.DELETE_PART, 'warehouse_worker must not delete parts');

  allow(ROLES.PRICING_MANAGER, ACTIONS.EDIT_PRICE, 'pricing_manager must edit price');
  allow(ROLES.PRICING_MANAGER, ACTIONS.MARK_PRICE_READY, 'pricing_manager must mark price ready');
  deny(ROLES.PRICING_MANAGER, ACTIONS.APPROVE_SELLER, 'pricing_manager must not approve sellers');
  deny(ROLES.PRICING_MANAGER, ACTIONS.MANAGE_LOCATIONS, 'pricing_manager must not change warehouse capacity');

  allow(ROLES.SALES_OPERATOR, ACTIONS.CREATE_RESERVATION, 'sales_operator must create reservation');
  allow(ROLES.SALES_OPERATOR, ACTIONS.CONVERT_RESERVATION_TO_ORDER, 'sales_operator must convert reservation to order');
  deny(ROLES.SALES_OPERATOR, ACTIONS.EDIT_TAX_PROFILE, 'sales_operator must not edit tax mode');

  allow(ROLES.READ_ONLY_AUDITOR, ACTIONS.VIEW_AUDIT_LOGS, 'auditor must view audit logs');
  deny(ROLES.READ_ONLY_AUDITOR, ACTIONS.CREATE_PART, 'auditor must not mutate records');
  deny(ROLES.READ_ONLY_AUDITOR, ACTIONS.UPDATE_PAYMENT_STATUS, 'auditor must not update payment');

  const unauthenticated = permissionDecision({ role: null, action: ACTIONS.CREATE_PART });
  assert(unauthenticated.allowed === false, 'unauthenticated user must be denied');
  assert(unauthenticated.reason === 'unauthenticated', 'unauthenticated denial reason must be explicit');

  const tenantMismatch = permissionDecision({
    role: ROLES.SELLER_ADMIN,
    action: ACTIONS.CREATE_PART,
    userSellerId: 'seller_a',
    entitySellerId: 'seller_b'
  });
  assert(tenantMismatch.allowed === false, 'seller_admin must not access another seller tenant');
  assert(tenantMismatch.reason === 'tenant_mismatch', 'tenant mismatch reason must be explicit');

  const priceDecision = permissionDecision({
    role: ROLES.PRICING_MANAGER,
    action: ACTIONS.EDIT_PRICE,
    userSellerId: 'seller_a',
    entitySellerId: 'seller_a'
  });
  assert(priceDecision.allowed === true, 'pricing_manager must be allowed for own tenant');
  assert(priceDecision.audit_required === true, 'price mutation must require audit');

  console.log('Permission model tests passed');
}

run();
