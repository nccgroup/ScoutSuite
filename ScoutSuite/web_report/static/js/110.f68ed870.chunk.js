(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[110],{553:function(e,t,n){"use strict";n.r(t);var a=n(1),r=(n(0),n(697)),i=n(66),c=n(68),s=function(e){return Object(i.l)(e,"",(function(e){return t=e,Object(a.jsx)(c.a,{service:"virtualmachines",resource:"instances",id:t});var t}))};t.default=function(e){var t=e.subnet;return Object(a.jsxs)("div",{children:[Object(a.jsx)(r.c,{label:"Address Prefix",valuePath:"address_prefix",renderValue:i.q}),Object(a.jsx)(r.c,{label:"Address Prefixes",valuePath:"address_prefixes",renderValue:i.q}),Object(a.jsx)(r.c,{label:"Provisioning State",valuePath:"provisioning_state",renderValue:i.q}),Object(a.jsx)(r.c,{label:"Route Table",valuePath:"route_table",renderValue:i.q}),Object(a.jsx)(r.c,{label:"Interface Endpoints",valuePath:"interface_endpoints",renderValue:i.q}),Object(a.jsx)(r.c,{label:"IP Configuration Profiles",valuePath:"ip_configuration_profiles",renderValue:i.q}),Object(a.jsx)(r.c,{label:"Service Endpoints",valuePath:"service_endpoints",renderValue:i.q}),Object(a.jsx)(r.c,{label:"Service Endpoint Policies",valuePath:"service_endpoint_policies",renderValue:i.q}),Object(a.jsx)(r.c,{label:"Service Association Links",valuePath:"service_association_links",renderValue:i.q}),Object(a.jsx)(r.c,{label:"Resource Navigation Links",valuePath:"resource_navigation_links",renderValue:i.q}),Object(a.jsx)(r.c,{label:"Delegations",valuePath:"delegations",renderValue:i.q}),Object(a.jsx)(r.c,{label:"Purpose",valuePath:"purpose",renderValue:i.q}),Object(a.jsx)("br",{}),Object(a.jsx)("h5",{children:"Instances"}),s(t.instances)]})}},694:function(e,t,n){"use strict";n.d(t,"a",(function(){return c})),n.d(t,"b",(function(){return s})),n.d(t,"c",(function(){return o}));var a=n(0),r=n.n(a),i={path_to_issue:[],item:{}},c=r.a.createContext(i),s=r.a.createContext(""),o=r.a.createContext((function(){}))},695:function(e,t,n){"use strict";var a=n(1),r=n(0),i=n(694),c=n(66);t.a=function(e){var t=e.path,n=e.children,s=Object(r.useContext)(i.b);return Object(a.jsx)(i.b.Provider,{value:Object(c.a)(s,t),children:n})}},696:function(e,t,n){"use strict";var a=n(11),r=n(1),i=n(0),c=n(690),s=n(7),o=n.n(s),l=n(13),u=n.n(l),d=n(10),b=n.n(d),v=n(694),j=n(66),f=n(67),p=(n(698),n(686)),x=n(204),h=n.n(x),O=n(699),P=n.n(O),g=n(205),m=n(140),_=function(e){var t=e.service,n=e.finding,a=e.path,s=Object(i.useContext)(m.a),o=s.exceptions,l=s.addException,d=s.removeException,b=Object(g.b)().enqueueSnackbar,v=u()(o,[t,n],[]).includes(a);return Object(r.jsx)(c.a,{title:v?"Remove finding from exceptions list":"Add finding to exceptions list",placement:"top",arrow:!0,children:Object(r.jsx)(p.a,{size:"small",className:"exception-btn",onClick:v?function(){d(t,n,a),b("Exception removed.",{variant:"error",anchorOrigin:{vertical:"bottom",horizontal:"right"}})}:function(){l(t,n,a),b("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:v?Object(r.jsx)(P.a,{}):Object(r.jsx)(h.a,{})})})},V=n(30),q=function(e){var t,n=e.label,s=e.separator,l=e.valuePath,d=e.errorPath,p=e.className,x=e.inline,h=e.tooltip,O=e.tooltipProps,P=e.renderValue,g=e.basePathOverwrite,m=Object(V.g)(),q=Object(i.useContext)(v.a),C=Object(i.useContext)(v.b),E=Object(i.useContext)(v.c),k=Object(j.a)(g||C,l),A=P(e.value||u()(q.item,k,e.value));("boolean"===typeof A&&(A=String(A)),d)?t=(b()(d)?d:[d]).map((function(e){return Object(j.a)(g||C,e)})):t=[k];var S=t.some((function(e){return q.path_to_issues.includes(e)})),N=q.level;if(Object(i.useEffect)((function(){S&&E(N)}),[N]),void 0===A||null===A)return null;var R=Object(r.jsx)(_,{service:m.service,finding:m.finding,path:"".concat(q.path,".").concat(t[0])}),w=Object(r.jsxs)("span",{className:o()(S&&o()("issue",N)),children:[A,S&&R]});return Object(r.jsx)(f.a,{className:o()(p,"partial-value",{inline:x}),label:n,separator:s,value:h?Object(r.jsx)(c.a,Object(a.a)(Object(a.a)({title:A},O),{},{children:w})):w})};q.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=q},697:function(e,t,n){"use strict";n.d(t,"a",(function(){return i})),n.d(t,"b",(function(){return c.a})),n.d(t,"c",(function(){return s.a}));var a=n(1),r=(n(0),n(694)),i=(n(66),function(e){var t=e.data,n=e.children;return console.info("PARTIAL DATA",t),Object(a.jsx)(r.a.Provider,{value:t,children:n})}),c=n(695),s=n(696)},698:function(e,t,n){},699:function(e,t,n){"use strict";var a=n(35),r=n(37);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var i=r(n(0)),c=(0,a(n(38)).default)(i.createElement("path",{d:"M19 13H5v-2h14v2z"}),"Remove");t.default=c}}]);
//# sourceMappingURL=110.f68ed870.chunk.js.map