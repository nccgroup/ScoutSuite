(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[95],{534:function(e,t,a){"use strict";a.r(t);var n=a(1),c=(a(0),a(697)),r=a(66);t.default=function(){return Object(n.jsxs)(n.Fragment,{children:[Object(n.jsx)(c.c,{label:"ARN",valuePath:"arn"}),Object(n.jsx)(c.c,{label:"ID",valuePath:"id"}),Object(n.jsx)(c.c,{label:"Region",valuePath:"region"}),Object(n.jsx)(c.c,{label:"Availability Zone",valuePath:"availability_zone"}),Object(n.jsx)(c.c,{label:"VPC",valuePath:"vpc"}),Object(n.jsx)(c.c,{label:"Reservation ID",valuePath:"reservation_id"}),Object(n.jsx)(c.c,{label:"IAM role",valuePath:"iam_role",renderValue:r.q}),Object(n.jsx)(c.c,{label:"Monitoring",valuePath:"monitoring_enabled",renderValue:r.c}),Object(n.jsx)(c.c,{label:"Access Key Name",valuePath:"KeyName"}),Object(n.jsx)(c.c,{label:"State",valuePath:"State.Name"}),Object(n.jsx)(c.c,{label:"Instance Type",valuePath:"InstanceType"}),Object(n.jsx)(c.c,{label:"Up Since",valuePath:"LaunchTime",renderValue:r.h})]})}},694:function(e,t,a){"use strict";a.d(t,"a",(function(){return i})),a.d(t,"b",(function(){return l})),a.d(t,"c",(function(){return o}));var n=a(0),c=a.n(n),r={path_to_issue:[],item:{}},i=c.a.createContext(r),l=c.a.createContext(""),o=c.a.createContext((function(){}))},695:function(e,t,a){"use strict";var n=a(1),c=a(0),r=a(694),i=a(66);t.a=function(e){var t=e.path,a=e.children,l=Object(c.useContext)(r.b);return Object(n.jsx)(r.b.Provider,{value:Object(i.a)(l,t),children:a})}},696:function(e,t,a){"use strict";var n=a(11),c=a(1),r=a(0),i=a(690),l=a(7),o=a.n(l),u=a(13),s=a.n(u),b=a(10),j=a.n(b),v=a(694),d=a(66),h=a(67),f=(a(698),a(686)),p=a(204),x=a.n(p),O=a(699),m=a.n(O),P=a(205),g=a(140),C=function(e){var t=e.service,a=e.finding,n=e.path,l=Object(r.useContext)(g.a),o=l.exceptions,u=l.addException,b=l.removeException,j=Object(P.b)().enqueueSnackbar,v=s()(o,[t,a],[]).includes(n);return Object(c.jsx)(i.a,{title:v?"Remove finding from exceptions list":"Add finding to exceptions list",placement:"top",arrow:!0,children:Object(c.jsx)(f.a,{size:"small",className:"exception-btn",onClick:v?function(){b(t,a,n),j("Exception removed.",{variant:"error",anchorOrigin:{vertical:"bottom",horizontal:"right"}})}:function(){u(t,a,n),j("Exception added. Don't forget to export the exceptions!",{variant:"success",anchorOrigin:{vertical:"bottom",horizontal:"right"}})},children:v?Object(c.jsx)(m.a,{}):Object(c.jsx)(x.a,{})})})},_=a(30),y=function(e){var t,a=e.label,l=e.separator,u=e.valuePath,b=e.errorPath,f=e.className,p=e.inline,x=e.tooltip,O=e.tooltipProps,m=e.renderValue,P=e.basePathOverwrite,g=Object(_.g)(),y=Object(r.useContext)(v.a),A=Object(r.useContext)(v.b),N=Object(r.useContext)(v.c),E=Object(d.a)(P||A,u),I=m(e.value||s()(y.item,E,e.value));("boolean"===typeof I&&(I=String(I)),b)?t=(j()(b)?b:[b]).map((function(e){return Object(d.a)(P||A,e)})):t=[E];var R=t.some((function(e){return y.path_to_issues.includes(e)})),V=y.level;if(Object(r.useEffect)((function(){R&&N(V)}),[V]),void 0===I||null===I)return null;var z=Object(c.jsx)(C,{service:g.service,finding:g.finding,path:"".concat(y.path,".").concat(t[0])}),D=Object(c.jsxs)("span",{className:o()(R&&o()("issue",V)),children:[I,R&&z]});return Object(c.jsx)(h.a,{className:o()(f,"partial-value",{inline:p}),label:a,separator:l,value:x?Object(c.jsx)(i.a,Object(n.a)(Object(n.a)({title:I},O),{},{children:D})):D})};y.defaultProps={label:"",separator:": ",value:null,valuePath:null,errorPath:null,inline:!1,tooltip:!1,tooltipProps:{enterDelay:1e3,placement:"top-start"},renderValue:function(e){return e}};t.a=y},697:function(e,t,a){"use strict";a.d(t,"a",(function(){return r})),a.d(t,"b",(function(){return i.a})),a.d(t,"c",(function(){return l.a}));var n=a(1),c=(a(0),a(694)),r=(a(66),function(e){var t=e.data,a=e.children;return console.info("PARTIAL DATA",t),Object(n.jsx)(c.a.Provider,{value:t,children:a})}),i=a(695),l=a(696)},698:function(e,t,a){},699:function(e,t,a){"use strict";var n=a(35),c=a(37);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var r=c(a(0)),i=(0,n(a(38)).default)(r.createElement("path",{d:"M19 13H5v-2h14v2z"}),"Remove");t.default=i}}]);
//# sourceMappingURL=95.51ef4106.chunk.js.map