(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[114],{646:function(e,s,n){"use strict";n.r(s);var t=n(1),r=(n(0),n(742)),a=n(739),c=n(91),i=n(744),u=n(72),l=n(750),o=n(748),j=function(e){return Object(c.l)(e,"",(function(e){return function(e){return Object(t.jsx)(u.a,{service:"aad",resource:"groups",id:e.id,name:e.name})}(e)}))},b=function(e){return Object(c.l)(e,"",(function(e){return function(e){return Object(t.jsx)(u.a,{service:"aad",resource:"users",id:e.id,name:e.name})}(e)}))},d=function(e){return Object(c.l)(e,"",(function(e){return function(e){return Object(t.jsx)(u.a,{service:"aad",resource:"service_principals",id:e.id,name:e.name})}(e)}))};s.default=function(e){var s=e.data,n=e.item,u=Object(l.a)("aad","users",n.assignments?n.assignments.users:[]).data,p=Object(l.a)("aad","groups",n.assignments?n.assignments.groups:[]).data,O=Object(l.a)("aad","service_principals",n.assignments?n.assignments.service_principals:[]).data;return s?Object(t.jsxs)(a.a,{data:s,children:[Object(t.jsxs)(r.a,{children:[Object(t.jsx)(a.c,{label:"ID",valuePath:"id",renderValue:c.q}),Object(t.jsx)(a.c,{label:"Description",valuePath:"description",renderValue:c.q}),Object(t.jsx)(a.c,{label:"Type",valuePath:"type",renderValue:c.q}),Object(t.jsx)(a.c,{label:"Role Type",valuePath:"role_type",renderValue:c.q}),Object(t.jsx)(a.c,{label:"Assignable Scopes",valuePath:"assignable_scopes",renderValue:c.q}),Object(t.jsx)(a.c,{label:"Custom Subscriptions Owner Roles",valuePath:"custom_subscription_owner_role"})]}),Object(t.jsxs)(i.b,{children:[Object(t.jsx)(i.a,{title:"Permissions",children:Object(t.jsx)(o.a,{name:"",policy:n.permissions,defaultOpen:!0})}),Object(t.jsxs)(i.a,{title:"Assignments",children:[n.assignments.users&&Object(t.jsxs)(t.Fragment,{children:[Object(t.jsx)(a.c,{label:"Users",errorPath:"users",value:""}),Object(t.jsx)("ul",{children:b(u)})]}),n.assignments.groups&&Object(t.jsxs)(t.Fragment,{children:[Object(t.jsx)(a.c,{label:"Groups",errorPath:"groups",value:""}),Object(t.jsx)("ul",{children:j(p)})]}),n.assignments.service_principals&&Object(t.jsxs)(t.Fragment,{children:[Object(t.jsx)(a.c,{label:"Service Principals",errorPath:"serviceprincipals",value:""}),Object(t.jsx)("ul",{children:d(O)})]})]})]})]}):null}},742:function(e,s,n){"use strict";var t=n(1);n(0),n(743);s.a=function(e){var s=e.children;return Object(t.jsxs)("div",{className:"informations-wrapper",children:[Object(t.jsx)("h4",{className:"title",children:"Informations"}),s]})}},743:function(e,s,n){},750:function(e,s,n){"use strict";n.d(s,"a",(function(){return l}));var t=n(37),r=n.n(t),a=n(73),c=n(15),i=n(0),u=n(152),l=function(e,s,n){var t=Object(i.useState)([]),l=Object(c.a)(t,2),o=l[0],j=l[1],b=Object(i.useState)(!0),d=Object(c.a)(b,2),p=d[0],O=d[1];return Object(i.useEffect)((function(){(function(){var t=Object(a.a)(r.a.mark((function t(){var a,c;return r.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(!(e&&s&&n)){t.next=15;break}return O(!0),t.prev=2,a=n.map((function(n){return u.b("services/".concat(e,"/resources/").concat(s,"/").concat(n))})),t.next=6,Promise.all(a);case 6:c=t.sent,console.info("useResources response",e,s,n,c),j(c),t.next=14;break;case 11:t.prev=11,t.t0=t.catch(2),console.error(t.t0.message);case 14:O(!1);case 15:case"end":return t.stop()}}),t,null,[[2,11]])})));return function(){return t.apply(this,arguments)}})()()}),[n]),{data:o,loading:p}}}}]);
//# sourceMappingURL=114.a1c8a8c8.chunk.js.map