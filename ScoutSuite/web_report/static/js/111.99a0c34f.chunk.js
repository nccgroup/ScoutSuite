(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[111],{582:function(e,n,t){"use strict";t.r(n);var i=t(1),c=t(18),a=(t(0),t(13)),r=t.n(a),s=t(29),l=t.n(s),o=t(66),j=t(697),u=t(702),b=t(700),d=t(704),h=t(706),m=t(68);n.default=function(e){var n=e.data;if(!n)return null;var t=r()(n,["item","users"],[]),a=r()(n,["item","inline_policies"],{}),s=r()(n,["item","policies"],[]);return Object(i.jsxs)(j.a,{data:n,children:[Object(i.jsxs)(b.a,{children:[Object(i.jsx)(j.c,{label:"ARN",valuePath:"arn",renderValue:o.q}),Object(i.jsx)(j.c,{label:"Creation Date",valuePath:"CreateDate",renderValue:o.h})]}),Object(i.jsxs)(u.b,{children:[Object(i.jsx)(u.a,{title:"Members",children:l()(t)?Object(i.jsx)(j.c,{errorPath:"ALL",renderValue:function(){return Object(i.jsx)(d.a,{message:"This group has no members."})}}):Object(o.l)(t,"",(function(e){return Object(i.jsx)(m.a,{service:"iam",resource:"users",id:e})}))}),Object(i.jsx)(u.a,{title:"Inline Policies",disabled:l()(a),children:Object(i.jsx)(i.Fragment,{children:Object.entries(a).map((function(e,n){var t=Object(c.a)(e,2),a=t[0],r=t[1];return Object(i.jsx)(h.a,{name:r.name,policy:r.PolicyDocument,policyPath:"inline_policies.".concat(a,".PolicyDocument")},n)}))})}),Object(i.jsx)(u.a,{title:"Managed Policies",disabled:l()(s),children:Object(o.l)(s,"",o.m)})]})]})}},700:function(e,n,t){"use strict";var i=t(1);t(0),t(701);n.a=function(e){var n=e.children;return Object(i.jsxs)("div",{className:"informations-wrapper",children:[Object(i.jsx)("h4",{className:"title",children:"Informations"}),n]})}},701:function(e,n,t){},704:function(e,n,t){"use strict";var i=t(1),c=(t(0),t(7)),a=t.n(c),r=t(115),s=t.n(r),l=(t(705),{icon:Object(i.jsx)(s.a,{fontSize:"inherit"})}),o=function(e){var n=e.message,t=e.icon,c=e.className;return Object(i.jsxs)("div",{className:a()("warning-message",c),children:[t,n]})};o.defaultProps=l,n.a=o},705:function(e,n,t){}}]);
//# sourceMappingURL=111.99a0c34f.chunk.js.map