# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

from datadog_checks.linkerd import LinkerdCheck

# 3p
import mock
import pytest


LINKERD_FIXTURE_METRICS = {
    'jvm:start_time': 'jvm.start_time',
    'jvm:application_time_millis': 'jvm.application_time_millis',
    'jvm:classes:total_loaded': 'jvm.classes.total_loaded',
    'jvm:classes:current_loaded': 'jvm.classes.current_loaded',
    'jvm:classes:total_unloaded': 'jvm.classes.total_unloaded',
    'jvm:postGC:Par_Survivor_Space:max': 'jvm.postGC.Par_Survivor_Space.max',
    'jvm:postGC:Par_Survivor_Space:used': 'jvm.postGC.Par_Survivor_Space.used',
    'jvm:postGC:CMS_Old_Gen:max': 'jvm.postGC.CMS_Old_Gen.max',
    'jvm:postGC:CMS_Old_Gen:used': 'jvm.postGC.CMS_Old_Gen.used',
    'jvm:postGC:Par_Eden_Space:max': 'jvm.postGC.Par_Eden_Space.max',
    'jvm:postGC:Par_Eden_Space:used': 'jvm.postGC.Par_Eden_Space.used',
    'jvm:postGC:used': 'jvm.postGC.used',
    'jvm:nonheap:committed': 'jvm.nonheap.committed',
    'jvm:nonheap:max': 'jvm.nonheap.max',
    'jvm:nonheap:used': 'jvm.nonheap.used',
    'jvm:tenuring_threshold': 'jvm.tenuring_threshold',
    'jvm:thread:daemon_count': 'jvm.thread.daemon_count',
    'jvm:thread:count': 'jvm.thread.count',
    'jvm:thread:peak_count': 'jvm.thread.peak_count',
    'jvm:mem:postGC:Par_Survivor_Space:max': 'jvm.mem.postGC.Par_Survivor_Space.max',
    'jvm:mem:postGC:Par_Survivor_Space:used': 'jvm.mem.postGC.Par_Survivor_Space.used',
    'jvm:mem:postGC:CMS_Old_Gen:max': 'jvm.mem.postGC.CMS_Old_Gen.max',
    'jvm:mem:postGC:CMS_Old_Gen:used': 'jvm.mem.postGC.CMS_Old_Gen.used',
    'jvm:mem:postGC:Par_Eden_Space:max': 'jvm.mem.postGC.Par_Eden_Space.max',
    'jvm:mem:postGC:Par_Eden_Space:used': 'jvm.mem.postGC.Par_Eden_Space.used',
    'jvm:mem:postGC:used': 'jvm.mem.postGC.used',
    'jvm:mem:metaspace:max_capacity': 'jvm.mem.metaspace.max_capacity',
    'jvm:mem:buffer:direct:max': 'jvm.mem.buffer.direct.max',
    'jvm:mem:buffer:direct:count': 'jvm.mem.buffer.direct.count',
    'jvm:mem:buffer:direct:used': 'jvm.mem.buffer.direct.used',
    'jvm:mem:buffer:mapped:max': 'jvm.mem.buffer.mapped.max',
    'jvm:mem:buffer:mapped:count': 'jvm.mem.buffer.mapped.count',
    'jvm:mem:buffer:mapped:used': 'jvm.mem.buffer.mapped.used',
    'jvm:mem:allocations:eden:bytes': 'jvm.mem.allocations.eden.bytes',
    'jvm:mem:current:used': 'jvm.mem.current.used',
    'jvm:mem:current:CMS_Old_Gen:max': 'jvm.mem.current.CMS_Old_Gen.max',
    'jvm:mem:current:CMS_Old_Gen:used': 'jvm.mem.current.CMS_Old_Gen.used',
    'jvm:mem:current:Metaspace:max': 'jvm.mem.current.Metaspace.max',
    'jvm:mem:current:Metaspace:used': 'jvm.mem.current.Metaspace.used',
    'jvm:mem:current:Par_Eden_Space:max': 'jvm.mem.current.Par_Eden_Space.max',
    'jvm:mem:current:Par_Eden_Space:used': 'jvm.mem.current.Par_Eden_Space.used',
    'jvm:mem:current:Par_Survivor_Space:max': 'jvm.mem.current.Par_Survivor_Space.max',
    'jvm:mem:current:Par_Survivor_Space:used': 'jvm.mem.current.Par_Survivor_Space.used',
    'jvm:mem:current:Compressed_Class_Space:max': 'jvm.mem.current.Compressed_Class_Space.max',
    'jvm:mem:current:Compressed_Class_Space:used': 'jvm.mem.current.Compressed_Class_Space.used',
    'jvm:mem:current:Code_Cache:max': 'jvm.mem.current.Code_Cache.max',
    'jvm:mem:current:Code_Cache:used': 'jvm.mem.current.Code_Cache.used',
    'jvm:num_cpus': 'jvm.num_cpus',
    'jvm:gc:msec': 'jvm.gc.msec',
    'jvm:gc:ParNew:msec': 'jvm.gc.ParNew.msec',
    'jvm:gc:ParNew:cycles': 'jvm.gc.ParNew.cycles',
    'jvm:gc:ConcurrentMarkSweep:msec': 'jvm.gc.ConcurrentMarkSweep.msec',
    'jvm:gc:ConcurrentMarkSweep:cycles': 'jvm.gc.ConcurrentMarkSweep.cycles',
    'jvm:gc:cycles': 'jvm.gc.cycles',
    'jvm:fd_limit': 'jvm.fd_limit',
    'jvm:compilation:time_msec': 'jvm.compilation.time_msec',
    'jvm:uptime': 'jvm.uptime',
    'jvm:safepoint:sync_time_millis': 'jvm.safepoint.sync_time_millis',
    'jvm:safepoint:total_time_millis': 'jvm.safepoint.total_time_millis',
    'jvm:safepoint:count': 'jvm.safepoint.count',
    'jvm:heap:committed': 'jvm.heap.committed',
    'jvm:heap:max': 'jvm.heap.max',
    'jvm:heap:used': 'jvm.heap.used',
    'jvm:fd_count': 'jvm.fd_count',
    'rt:server:sent_bytes': 'rt.server.sent_bytes',
    'rt:server:connects': 'rt.server.connects',
    'rt:server:success': 'rt.server.success',
    'rt:server:received_bytes': 'rt.server.received_bytes',
    'rt:server:read_timeout': 'rt.server.read_timeout',
    'rt:server:write_timeout': 'rt.server.write_timeout',
    'rt:server:nacks': 'rt.server.nacks',
    'rt:server:thread_usage:requests:mean': 'rt.server.thread_usage.requests.mean',
    'rt:server:thread_usage:requests:relative_stddev': 'rt.server.thread_usage.requests.relative_stddev',
    'rt:server:thread_usage:requests:stddev': 'rt.server.thread_usage.requests.stddev',
    'rt:server:socket_unwritable_ms': 'rt.server.socket_unwritable_ms',
    'rt:server:closes': 'rt.server.closes',
    'rt:server:status:1XX': 'rt.server.status.1XX',
    'rt:server:status:4XX': 'rt.server.status.4XX',
    'rt:server:status:2XX': 'rt.server.status.2XX',
    'rt:server:status:error': 'rt.server.status.error',
    'rt:server:status:3XX': 'rt.server.status.3XX',
    'rt:server:status:5XX': 'rt.server.status.5XX',
    'rt:server:status:200': 'rt.server.status.200',
    'rt:server:nonretryable_nacks': 'rt.server.nonretryable_nacks',
    'rt:server:socket_writable_ms': 'rt.server.socket_writable_ms',
    'rt:server:requests': 'rt.server.requests',
    'rt:server:pending': 'rt.server.pending',
    'rt:server:connections': 'rt.server.connections',
    'rt:service:success': 'rt.service.success',
    'rt:service:retries:total': 'rt.service.retries.total',
    'rt:service:retries:budget_exhausted': 'rt.service.retries.budget_exhausted',
    'rt:service:retries:budget': 'rt.service.retries.budget',
    'rt:service:requests': 'rt.service.requests',
    'rt:service:pending': 'rt.service.pending',
    'rt:client:sent_bytes': 'rt.client.sent_bytes',
    'rt:client:failure_accrual:removals': 'rt.client.failure_accrual.removals',
    'rt:client:failure_accrual:probes': 'rt.client.failure_accrual.probes',
    'rt:client:failure_accrual:removed_for_ms': 'rt.client.failure_accrual.removed_for_ms',
    'rt:client:failure_accrual:revivals': 'rt.client.failure_accrual.revivals',
    'rt:client:connects': 'rt.client.connects',
    'rt:client:pool_num_waited': 'rt.client.pool_num_waited',
    'rt:client:success': 'rt.client.success',
    'rt:client:pool_waiters': 'rt.client.pool_waiters',
    'rt:client:retries:request_limit': 'rt.client.retries.request_limit',
    'rt:client:retries:budget_exhausted': 'rt.client.retries.budget_exhausted',
    'rt:client:retries:cannot_retry': 'rt.client.retries.cannot_retry',
    'rt:client:retries:not_open': 'rt.client.retries.not_open',
    'rt:client:retries:budget': 'rt.client.retries.budget',
    'rt:client:retries:requeues': 'rt.client.retries.requeues',
    'rt:client:received_bytes': 'rt.client.received_bytes',
    'rt:client:read_timeout': 'rt.client.read_timeout',
    'rt:client:write_timeout': 'rt.client.write_timeout',
    'rt:client:service:success': 'rt.client.service.success',
    'rt:client:service:pending': 'rt.client.service.pending',
    'rt:client:service:requests': 'rt.client.service.requests',
    'rt:client:pool_num_too_many_waiters': 'rt.client.pool_num_too_many_waiters',
    'rt:client:socket_unwritable_ms': 'rt.client.socket_unwritable_ms',
    'rt:client:closes': 'rt.client.closes',
    'rt:client:pool_cached': 'rt.client.pool_cached',
    'rt:client:nack_admission_control:dropped_requests': 'rt.client.nack_admission_control.dropped_requests',
    'rt:client:status:1XX': 'rt.client.status.1XX',
    'rt:client:status:4XX': 'rt.client.status.4XX',
    'rt:client:status:2XX': 'rt.client.status.2XX',
    'rt:client:status:error': 'rt.client.status.error',
    'rt:client:status:3XX': 'rt.client.status.3XX',
    'rt:client:status:5XX': 'rt.client.status.5XX',
    'rt:client:status:200': 'rt.client.status.200',
    'rt:client:pool_size': 'rt.client.pool_size',
    'rt:client:available': 'rt.client.available',
    'rt:client:socket_writable_ms': 'rt.client.socket_writable_ms',
    'rt:client:cancelled_connects': 'rt.client.cancelled_connects',
    'rt:client:requests': 'rt.client.requests',
    'rt:client:loadbalancer:size': 'rt.client.loadbalancer.size',
    'rt:client:loadbalancer:rebuilds': 'rt.client.loadbalancer.rebuilds',
    'rt:client:loadbalancer:closed': 'rt.client.loadbalancer.closed',
    'rt:client:loadbalancer:load': 'rt.client.loadbalancer.load',
    'rt:client:loadbalancer:meanweight': 'rt.client.loadbalancer.meanweight',
    'rt:client:loadbalancer:adds': 'rt.client.loadbalancer.adds',
    'rt:client:loadbalancer:updates': 'rt.client.loadbalancer.updates',
    'rt:client:loadbalancer:algorithm:p2c_least_loaded': 'rt.client.loadbalancer.algorithm.p2c_least_loaded',
    'rt:client:loadbalancer:available': 'rt.client.loadbalancer.available',
    'rt:client:loadbalancer:max_effort_exhausted': 'rt.client.loadbalancer.max_effort_exhausted',
    'rt:client:loadbalancer:busy': 'rt.client.loadbalancer.busy',
    'rt:client:loadbalancer:removes': 'rt.client.loadbalancer.removes',
    'rt:client:pending': 'rt.client.pending',
    'rt:client:dispatcher:serial:queue_size': 'rt.client.dispatcher.serial.queue_size',
    'rt:client:connections': 'rt.client.connections',
    'rt:bindcache:path:expires': 'rt.bindcache.path.expires',
    'rt:bindcache:path:evicts': 'rt.bindcache.path.evicts',
    'rt:bindcache:path:misses': 'rt.bindcache.path.misses',
    'rt:bindcache:path:oneshots': 'rt.bindcache.path.oneshots',
    'rt:bindcache:bound:expires': 'rt.bindcache.bound.expires',
    'rt:bindcache:bound:evicts': 'rt.bindcache.bound.evicts',
    'rt:bindcache:bound:misses': 'rt.bindcache.bound.misses',
    'rt:bindcache:bound:oneshots': 'rt.bindcache.bound.oneshots',
    'rt:bindcache:tree:expires': 'rt.bindcache.tree.expires',
    'rt:bindcache:tree:evicts': 'rt.bindcache.tree.evicts',
    'rt:bindcache:tree:misses': 'rt.bindcache.tree.misses',
    'rt:bindcache:tree:oneshots': 'rt.bindcache.tree.oneshots',
    'rt:bindcache:client:expires': 'rt.bindcache.client.expires',
    'rt:bindcache:client:evicts': 'rt.bindcache.client.evicts',
    'rt:bindcache:client:misses': 'rt.bindcache.client.misses',
    'rt:bindcache:client:oneshots': 'rt.bindcache.client.oneshots',
}

LINKERD_FIXTURE_TYPES = {
    'jvm:start_time': 'gauge',
    'jvm:application_time_millis': 'gauge',
    'jvm:classes:total_loaded': 'gauge',
    'jvm:classes:current_loaded': 'gauge',
    'jvm:classes:total_unloaded': 'gauge',
    'jvm:postGC:Par_Survivor_Space:max': 'gauge',
    'jvm:postGC:Par_Survivor_Space:used': 'gauge',
    'jvm:postGC:CMS_Old_Gen:max': 'gauge',
    'jvm:postGC:CMS_Old_Gen:used': 'gauge',
    'jvm:postGC:Par_Eden_Space:max': 'gauge',
    'jvm:postGC:Par_Eden_Space:used': 'gauge',
    'jvm:postGC:used': 'gauge',
    'jvm:nonheap:committed': 'gauge',
    'jvm:nonheap:max': 'gauge',
    'jvm:nonheap:used': 'gauge',
    'jvm:tenuring_threshold': 'gauge',
    'jvm:thread:daemon_count': 'gauge',
    'jvm:thread:count': 'gauge',
    'jvm:thread:peak_count': 'gauge',
    'jvm:mem:postGC:Par_Survivor_Space:max': 'gauge',
    'jvm:mem:postGC:Par_Survivor_Space:used': 'gauge',
    'jvm:mem:postGC:CMS_Old_Gen:max': 'gauge',
    'jvm:mem:postGC:CMS_Old_Gen:used': 'gauge',
    'jvm:mem:postGC:Par_Eden_Space:max': 'gauge',
    'jvm:mem:postGC:Par_Eden_Space:used': 'gauge',
    'jvm:mem:postGC:used': 'gauge',
    'jvm:mem:metaspace:max_capacity': 'gauge',
    'jvm:mem:buffer:direct:max': 'gauge',
    'jvm:mem:buffer:direct:count': 'gauge',
    'jvm:mem:buffer:direct:used': 'gauge',
    'jvm:mem:buffer:mapped:max': 'gauge',
    'jvm:mem:buffer:mapped:count': 'gauge',
    'jvm:mem:buffer:mapped:used': 'gauge',
    'jvm:mem:allocations:eden:bytes': 'gauge',
    'jvm:mem:current:used': 'gauge',
    'jvm:mem:current:CMS_Old_Gen:max': 'gauge',
    'jvm:mem:current:CMS_Old_Gen:used': 'gauge',
    'jvm:mem:current:Metaspace:max': 'gauge',
    'jvm:mem:current:Metaspace:used': 'gauge',
    'jvm:mem:current:Par_Eden_Space:max': 'gauge',
    'jvm:mem:current:Par_Eden_Space:used': 'gauge',
    'jvm:mem:current:Par_Survivor_Space:max': 'gauge',
    'jvm:mem:current:Par_Survivor_Space:used': 'gauge',
    'jvm:mem:current:Compressed_Class_Space:max': 'gauge',
    'jvm:mem:current:Compressed_Class_Space:used': 'gauge',
    'jvm:mem:current:Code_Cache:max': 'gauge',
    'jvm:mem:current:Code_Cache:used': 'gauge',
    'jvm:num_cpus': 'gauge',
    'jvm:gc:msec': 'gauge',
    'jvm:gc:ParNew:msec': 'gauge',
    'jvm:gc:ParNew:cycles': 'gauge',
    'jvm:gc:ConcurrentMarkSweep:msec': 'gauge',
    'jvm:gc:ConcurrentMarkSweep:cycles': 'gauge',
    'jvm:gc:cycles': 'gauge',
    'jvm:fd_limit': 'gauge',
    'jvm:compilation:time_msec': 'gauge',
    'jvm:uptime': 'gauge',
    'jvm:safepoint:sync_time_millis': 'gauge',
    'jvm:safepoint:total_time_millis': 'gauge',
    'jvm:safepoint:count': 'gauge',
    'jvm:heap:committed': 'gauge',
    'jvm:heap:max': 'gauge',
    'jvm:heap:used': 'gauge',
    'jvm:fd_count': 'gauge',
    'rt:server:sent_bytes': 'gauge',
    'rt:server:connects': 'gauge',
    'rt:server:success': 'gauge',
    'rt:server:received_bytes': 'gauge',
    'rt:server:read_timeout': 'gauge',
    'rt:server:write_timeout': 'gauge',
    'rt:server:nacks': 'gauge',
    'rt:server:thread_usage:requests:mean': 'gauge',
    'rt:server:thread_usage:requests:relative_stddev': 'gauge',
    'rt:server:thread_usage:requests:stddev': 'gauge',
    'rt:server:socket_unwritable_ms': 'gauge',
    'rt:server:closes': 'gauge',
    'rt:server:status:1XX': 'gauge',
    'rt:server:status:4XX': 'gauge',
    'rt:server:status:2XX': 'gauge',
    'rt:server:status:error': 'gauge',
    'rt:server:status:3XX': 'gauge',
    'rt:server:status:5XX': 'gauge',
    'rt:server:status:200': 'gauge',
    'rt:server:nonretryable_nacks': 'gauge',
    'rt:server:socket_writable_ms': 'gauge',
    'rt:server:requests': 'gauge',
    'rt:server:pending': 'gauge',
    'rt:server:connections': 'gauge',
    'rt:service:success': 'gauge',
    'rt:service:retries:total': 'gauge',
    'rt:service:retries:budget_exhausted': 'gauge',
    'rt:service:retries:budget': 'gauge',
    'rt:service:requests': 'gauge',
    'rt:service:pending': 'gauge',
    'rt:client:sent_bytes': 'gauge',
    'rt:client:failure_accrual:removals': 'gauge',
    'rt:client:failure_accrual:probes': 'gauge',
    'rt:client:failure_accrual:removed_for_ms': 'gauge',
    'rt:client:failure_accrual:revivals': 'gauge',
    'rt:client:connects': 'gauge',
    'rt:client:pool_num_waited': 'gauge',
    'rt:client:success': 'gauge',
    'rt:client:pool_waiters': 'gauge',
    'rt:client:retries:request_limit': 'gauge',
    'rt:client:retries:budget_exhausted': 'gauge',
    'rt:client:retries:cannot_retry': 'gauge',
    'rt:client:retries:not_open': 'gauge',
    'rt:client:retries:budget': 'gauge',
    'rt:client:retries:requeues': 'gauge',
    'rt:client:received_bytes': 'gauge',
    'rt:client:read_timeout': 'gauge',
    'rt:client:write_timeout': 'gauge',
    'rt:client:service:success': 'gauge',
    'rt:client:service:pending': 'gauge',
    'rt:client:service:requests': 'gauge',
    'rt:client:pool_num_too_many_waiters': 'gauge',
    'rt:client:socket_unwritable_ms': 'gauge',
    'rt:client:closes': 'gauge',
    'rt:client:pool_cached': 'gauge',
    'rt:client:nack_admission_control:dropped_requests': 'gauge',
    'rt:client:status:1XX': 'gauge',
    'rt:client:status:4XX': 'gauge',
    'rt:client:status:2XX': 'gauge',
    'rt:client:status:error': 'gauge',
    'rt:client:status:3XX': 'gauge',
    'rt:client:status:5XX': 'gauge',
    'rt:client:status:200': 'gauge',
    'rt:client:pool_size': 'gauge',
    'rt:client:available': 'gauge',
    'rt:client:socket_writable_ms': 'gauge',
    'rt:client:cancelled_connects': 'gauge',
    'rt:client:requests': 'gauge',
    'rt:client:loadbalancer:size': 'gauge',
    'rt:client:loadbalancer:rebuilds': 'gauge',
    'rt:client:loadbalancer:closed': 'gauge',
    'rt:client:loadbalancer:load': 'gauge',
    'rt:client:loadbalancer:meanweight': 'gauge',
    'rt:client:loadbalancer:adds': 'gauge',
    'rt:client:loadbalancer:updates': 'gauge',
    'rt:client:loadbalancer:algorithm:p2c_least_loaded': 'gauge',
    'rt:client:loadbalancer:available': 'gauge',
    'rt:client:loadbalancer:max_effort_exhausted': 'gauge',
    'rt:client:loadbalancer:busy': 'gauge',
    'rt:client:loadbalancer:removes': 'gauge',
    'rt:client:pending': 'gauge',
    'rt:client:dispatcher:serial:queue_size': 'gauge',
    'rt:client:connections': 'gauge',
    'rt:bindcache:path:expires': 'gauge',
    'rt:bindcache:path:evicts': 'gauge',
    'rt:bindcache:path:misses': 'gauge',
    'rt:bindcache:path:oneshots': 'gauge',
    'rt:bindcache:bound:expires': 'gauge',
    'rt:bindcache:bound:evicts': 'gauge',
    'rt:bindcache:bound:misses': 'gauge',
    'rt:bindcache:bound:oneshots': 'gauge',
    'rt:bindcache:tree:expires': 'gauge',
    'rt:bindcache:tree:evicts': 'gauge',
    'rt:bindcache:tree:misses': 'gauge',
    'rt:bindcache:tree:oneshots': 'gauge',
    'rt:bindcache:client:expires': 'gauge',
    'rt:bindcache:client:evicts': 'gauge',
    'rt:bindcache:client:misses': 'gauge',
    'rt:bindcache:client:oneshots': 'gauge',
}

MOCK_INSTANCE = {
    'prometheus_url': 'http://fake.tld/prometheus',
    'metrics': [LINKERD_FIXTURE_METRICS],
    'type_overrides': LINKERD_FIXTURE_TYPES,
}

LINKERD_FIXTURE_VALUES = {
    'linkerd.jvm.start_time': 1.52103079E12,
    'linkerd.jvm.application_time_millis': 52340.887,
    'linkerd.jvm.classes.total_loaded': 8842.0,
    'linkerd.jvm.classes.current_loaded': 8815.0,
    'linkerd.jvm.classes.total_unloaded': 27.0,
    'linkerd.jvm.postGC.Par_Survivor_Space.max': 1.7432576E7,
    'linkerd.jvm.postGC.Par_Survivor_Space.used': 200736.0,
    'linkerd.jvm.postGC.CMS_Old_Gen.max': 8.9928499E8,
    'linkerd.jvm.postGC.CMS_Old_Gen.used': 2.0269128E7,
    'linkerd.jvm.postGC.Par_Eden_Space.max': 1.3959168E8,
    'linkerd.jvm.postGC.Par_Eden_Space.used': 0.0,
    'linkerd.jvm.postGC.used': 2.0469864E7,
    'linkerd.jvm.nonheap.committed': 7.122944E7,
    'linkerd.jvm.nonheap.max': -1.0,
    'linkerd.jvm.nonheap.used': 6.564336E7,
    'linkerd.jvm.tenuring_threshold': 6.0,
    'linkerd.jvm.thread.daemon_count': 22.0,
    'linkerd.jvm.thread.count': 23.0,
    'linkerd.jvm.thread.peak_count': 24.0,
    'linkerd.jvm.mem.postGC.Par_Survivor_Space.max': 1.7432576E7,
    'linkerd.jvm.mem.postGC.Par_Survivor_Space.used': 200736.0,
    'linkerd.jvm.mem.postGC.CMS_Old_Gen.max': 8.9928499E8,
    'linkerd.jvm.mem.postGC.CMS_Old_Gen.used': 2.0269128E7,
    'linkerd.jvm.mem.postGC.Par_Eden_Space.max': 1.3959168E8,
    'linkerd.jvm.mem.postGC.Par_Eden_Space.used': 0.0,
    'linkerd.jvm.mem.postGC.used': 2.0469864E7,
    'linkerd.jvm.mem.metaspace.max_capacity': 1.10729626E9,
    'linkerd.jvm.mem.buffer.direct.max': 0.0,
    'linkerd.jvm.mem.buffer.direct.count': 1.0,
    'linkerd.jvm.mem.buffer.direct.used': 1.0,
    'linkerd.jvm.mem.buffer.mapped.max': 0.0,
    'linkerd.jvm.mem.buffer.mapped.count': 0.0,
    'linkerd.jvm.mem.buffer.mapped.used': 0.0,
    'linkerd.jvm.mem.allocations.eden.bytes': 1.22551552E9,
    'linkerd.jvm.mem.current.used': 9.0179664E7,
    'linkerd.jvm.mem.current.CMS_Old_Gen.max': 8.9928499E8,
    'linkerd.jvm.mem.current.CMS_Old_Gen.used': 2.2799416E7,
    'linkerd.jvm.mem.current.Metaspace.max': -1.0,
    'linkerd.jvm.mem.current.Metaspace.used': 5.1355408E7,
    'linkerd.jvm.mem.current.Par_Eden_Space.max': 1.3959168E8,
    'linkerd.jvm.mem.current.Par_Eden_Space.used': 1586640.0,
    'linkerd.jvm.mem.current.Par_Survivor_Space.max': 1.7432576E7,
    'linkerd.jvm.mem.current.Par_Survivor_Space.used': 200736.0,
    'linkerd.jvm.mem.current.Compressed_Class_Space.max': 1.07374182E9,
    'linkerd.jvm.mem.current.Compressed_Class_Space.used': 8188496.0,
    'linkerd.jvm.mem.current.Code_Cache.max': 5.0331648E7,
    'linkerd.jvm.mem.current.Code_Cache.used': 6099456.0,
    'linkerd.jvm.num_cpus': 2.0,
    'linkerd.jvm.gc.msec': 674.0,
    'linkerd.jvm.gc.ParNew.msec': 561.0,
    'linkerd.jvm.gc.ParNew.cycles': 163.0,
    'linkerd.jvm.gc.ConcurrentMarkSweep.msec': 113.0,
    'linkerd.jvm.gc.ConcurrentMarkSweep.cycles': 6.0,
    'linkerd.jvm.gc.cycles': 169.0,
    'linkerd.jvm.fd_limit': 1048576.0,
    'linkerd.jvm.compilation.time_msec': 18540.0,
    'linkerd.jvm.uptime': 53922.0,
    'linkerd.jvm.safepoint.sync_time_millis': 557.0,
    'linkerd.jvm.safepoint.total_time_millis': 1295.0,
    'linkerd.jvm.safepoint.count': 592.0,
    'linkerd.jvm.heap.committed': 4.3810816E7,
    'linkerd.jvm.heap.max': 1.05630925E9,
    'linkerd.jvm.heap.used': 2.5757896E7,
    'linkerd.jvm.fd_count': 165.0,
    'linkerd.rt.server.sent_bytes': 2901160,
    'linkerd.rt.server.connects': 50,
    'linkerd.rt.server.success': 17694,
    'linkerd.rt.server.received_bytes': 1565173,
    'linkerd.rt.server.read_timeout': 0,
    'linkerd.rt.server.write_timeout': 0,
    'linkerd.rt.server.nacks': 0,
    'linkerd.rt.server.thread_usage.requests.mean': 0.0,
    'linkerd.rt.server.thread_usage.requests.relative_stddev': 0.0,
    'linkerd.rt.server.thread_usage.requests.stddev': 0.0,
    'linkerd.rt.server.socket_unwritable_ms': 0,
    'linkerd.rt.server.closes': 0,
    'linkerd.rt.server.status.1XX': 0,
    'linkerd.rt.server.status.4XX': 0,
    'linkerd.rt.server.status.2XX': 17697,
    'linkerd.rt.server.status.error': 0,
    'linkerd.rt.server.status.3XX': 0,
    'linkerd.rt.server.status.5XX': 0,
    'linkerd.rt.server.status.200': 17697,
    'linkerd.rt.server.nonretryable_nacks': 0,
    'linkerd.rt.server.socket_writable_ms': 0,
    'linkerd.rt.server.requests': 17700,
    'linkerd.rt.server.pending': 12.0,
    'linkerd.rt.server.connections': 50.0,
    'linkerd.rt.service.success': 17700,
    'linkerd.rt.service.retries.total': 0,
    'linkerd.rt.service.retries.budget_exhausted': 0,
    'linkerd.rt.service.retries.budget': 1081.0,
    'linkerd.rt.service.requests': 17700,
    'linkerd.rt.service.pending': 12.0,
    'linkerd.rt.client.sent_bytes': 4715595,
    'linkerd.rt.client.failure_accrual.removals': 0,
    'linkerd.rt.client.failure_accrual.probes': 0,
    'linkerd.rt.client.failure_accrual.removed_for_ms': 0,
    'linkerd.rt.client.failure_accrual.revivals': 0,
    'linkerd.rt.client.connects': 65,
    'linkerd.rt.client.pool_num_waited': 0,
    'linkerd.rt.client.success': 17703,
    'linkerd.rt.client.pool_waiters': 0.0,
    'linkerd.rt.client.retries.request_limit': 0,
    'linkerd.rt.client.retries.budget_exhausted': 0,
    'linkerd.rt.client.retries.cannot_retry': 0,
    'linkerd.rt.client.retries.not_open': 0,
    'linkerd.rt.client.retries.budget': 944.0,
    'linkerd.rt.client.retries.requeues': 0,
    'linkerd.rt.client.received_bytes': 2159766,
    'linkerd.rt.client.read_timeout': 0,
    'linkerd.rt.client.write_timeout': 0,
    'linkerd.rt.client.service.success': 17703,
    'linkerd.rt.client.service.pending': 1.0,
    'linkerd.rt.client.service.requests': 17703,
    'linkerd.rt.client.pool_num_too_many_waiters': 0,
    'linkerd.rt.client.socket_unwritable_ms': 0,
    'linkerd.rt.client.closes': 0,
    'linkerd.rt.client.pool_cached': 50.0,
    'linkerd.rt.client.nack_admission_control.dropped_requests': 0,
    'linkerd.rt.client.status.1XX': 0,
    'linkerd.rt.client.status.4XX': 0,
    'linkerd.rt.client.status.2XX': 17703,
    'linkerd.rt.client.status.error': 0,
    'linkerd.rt.client.status.3XX': 0,
    'linkerd.rt.client.status.5XX': 0,
    'linkerd.rt.client.status.200': 17703,
    'linkerd.rt.client.pool_size': 10.0,
    'linkerd.rt.client.available': 10.0,
    'linkerd.rt.client.socket_writable_ms': 0,
    'linkerd.rt.client.cancelled_connects': 0,
    'linkerd.rt.client.requests': 17703,
    'linkerd.rt.client.loadbalancer.size': 10.0,
    'linkerd.rt.client.loadbalancer.rebuilds': 1,
    'linkerd.rt.client.loadbalancer.closed': 0.0,
    'linkerd.rt.client.loadbalancer.load': 11.0,
    'linkerd.rt.client.loadbalancer.meanweight': 1.0,
    'linkerd.rt.client.loadbalancer.adds': 10,
    'linkerd.rt.client.loadbalancer.updates': 1,
    'linkerd.rt.client.loadbalancer.algorithm.p2c_least_loaded': 1.0,
    'linkerd.rt.client.loadbalancer.available': 10.0,
    'linkerd.rt.client.loadbalancer.max_effort_exhausted': 0,
    'linkerd.rt.client.loadbalancer.busy': 0.0,
    'linkerd.rt.client.loadbalancer.removes': 0,
    'linkerd.rt.client.pending': 10.0,
    'linkerd.rt.client.dispatcher.serial.queue_size': 0.0,
    'linkerd.rt.client.connections': 52.0,
    'linkerd.rt.bindcache.path.expires': 0,
    'linkerd.rt.bindcache.path.evicts': 0,
    'linkerd.rt.bindcache.path.misses': 1,
    'linkerd.rt.bindcache.path.oneshots': 0,
    'linkerd.rt.bindcache.bound.expires': 0,
    'linkerd.rt.bindcache.bound.evicts': 0,
    'linkerd.rt.bindcache.bound.misses': 1,
    'linkerd.rt.bindcache.bound.oneshots': 0,
    'linkerd.rt.bindcache.tree.expires': 0,
    'linkerd.rt.bindcache.tree.evicts': 0,
    'linkerd.rt.bindcache.tree.misses': 1,
    'linkerd.rt.bindcache.tree.oneshots': 0,
    'linkerd.rt.bindcache.client.expires': 0,
    'linkerd.rt.bindcache.client.evicts': 0,
    'linkerd.rt.bindcache.client.misses': 1,
    'linkerd.rt.bindcache.client.oneshots': 0,
}

class MockResponse:
    """
    MockResponse is used to simulate the object requests.Response commonly returned by requests.get
    """

    def __init__(self, content, content_type):
        if isinstance(content, list):
            self.content = content
        else:
            self.content = [content]
        self.headers = {'Content-Type': content_type}

    def iter_lines(self, **_):
        content = self.content.pop(0)
        for elt in content.split("\n"):
            yield elt

    def close(self):
        pass

@pytest.fixture
def linkerd_fixture():
    metrics_file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'linkerd.txt')
    responses = []
    with open(metrics_file_path, 'rb') as f:
        responses.append(f.read())

    p = mock.patch('datadog_checks.checks.prometheus.Scraper.poll',
                   return_value=MockResponse(responses, 'text/plain'),
                   __name__="poll")
    yield p.start()
    p.stop()

@pytest.fixture
def aggregator():
    from datadog_checks.stubs import aggregator
    aggregator.reset()
    return aggregator

def test_linkerd(aggregator, linkerd_fixture):
    """
    Test the full check
    """
    c = LinkerdCheck('linkerd', None, {}, [MOCK_INSTANCE])
    c.check(MOCK_INSTANCE)

    for metric in LINKERD_FIXTURE_VALUES:
        aggregator.assert_metric(metric, LINKERD_FIXTURE_VALUES[metric])