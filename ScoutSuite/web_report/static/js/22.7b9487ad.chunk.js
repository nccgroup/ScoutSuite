(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[22,118],{579:function(e,t,c){"use strict";c.r(t);var n=c(1),r=(c(0),c(55));t.default=function(){return Object(n.jsxs)(n.Fragment,{children:[Object(n.jsx)(r.c,{label:"ARN",valuePath:"arn"}),Object(n.jsx)(r.c,{label:"VPC",valuePath:"vpc"}),Object(n.jsx)(r.c,{label:"DNS",valuePath:"DNSName"}),Object(n.jsx)(r.c,{label:"Scheme",valuePath:"Scheme",errorPath:"load_balancer_scheme"}),Object(n.jsx)(r.c,{label:"Type",valuePath:"Type"}),Object(n.jsx)(r.c,{label:"Availability zones",valuePath:"AvailabilityZones",renderValue:function(e){return Object(n.jsx)("ul",{children:e.map((function(e,t){return Object(n.jsx)("li",{children:"".concat(e.ZoneName," (").concat(e.SubnetId,")")},t)}))})}})]})}},620:function(e,t,c){"use strict";c.r(t);var n=c(1),r=c(14),a=c(12),i=(c(0),c(15)),l=c.n(i),s=c(29),o=c.n(s),j=c(20),u=c(21),b=c(772),d=c(55),h=c(43),O=c(764),v=c(761),f=c(579);t.default=function(e){var t=e.data,c=l()(t,["item","path"],""),i=Object(b.a)(c),s=Object(b.b)(c),x=Object(j.a)(Object(u.i)("services.elbv2.regions.".concat(i,".vpcs.").concat(s,".name"))),m=x.data,p=x.loading;if(!t||p)return null;o()(m)||(t.item.vpc="".concat(m," (").concat(s,")"));var P=l()(t,["item","listeners"],{}),S=l()(t,["item","attributes"],[]),y=l()(t,["item","security_groups"],{}),g=l()(t,["item","tags"],[]),N=l()(t,["item","isNetwork"]);return Object(n.jsxs)(d.a,{data:t,children:[Object(n.jsx)(v.a,{children:Object(n.jsx)(f.default,{})}),Object(n.jsx)("div",{children:Object(n.jsxs)(O.b,{children:[Object(n.jsx)(O.a,{title:"Listeners",children:Object(n.jsx)("ul",{children:Object.entries(P).map((function(e,t){var c=Object(a.a)(e,2),i=c[0],l=c[1];return Object(n.jsx)("li",{children:Object(n.jsx)(d.c,{value:Object(r.a)({port:i},l),errorPath:"listeners.".concat(i),renderValue:function(e){return e.SslPolicy?Object(n.jsxs)(n.Fragment,{children:["".concat(e.port," (").concat(e.Protocol,", "),Object(n.jsx)(d.c,{value:e.SslPolicy,errorPath:"listeners.".concat(e.port,".SslPolicy"),inline:!0}),")"]}):"".concat(e.port," (").concat(e.Protocol,")")}})},t)}))})}),Object(n.jsx)(O.a,{title:"Attributes",children:Object(n.jsx)("div",{children:S.map((function(e,t){var c=e.Key,r=e.Value;return Object(n.jsx)(d.c,{label:c,value:r,errorPath:"attributes.".concat(t)},t)}))})}),!N&&Object(n.jsx)(O.a,{title:"Security Groups",disabled:o()(y),children:Object(h.l)(y,"",h.o)}),!o()(g)&&Object(n.jsx)(O.a,{title:"Tags",children:Object(h.j)(g)})]})})]})}},761:function(e,t,c){"use strict";var n=c(1);c(0),c(762);t.a=function(e){var t=e.children;return Object(n.jsxs)("div",{className:"informations-wrapper",children:[Object(n.jsx)("h4",{className:"title",children:"Informations"}),t]})}},762:function(e,t,c){},763:function(e,t,c){},764:function(e,t,c){"use strict";c.d(t,"a",(function(){return u})),c.d(t,"b",(function(){return s.b}));var n=c(1),r=c(12),a=c(0),i=c(8),l=c.n(i),s=c(77),o=c(78),j=c(62),u=(c(763),function(e){var t=e.title,c=e.isSelected,i=e.disabled,u=e.onClick,b=e.children,d=Object(a.useState)(""),h=Object(r.a)(d,2),O=h[0],v=h[1],f=O?Object(n.jsxs)(n.Fragment,{children:[t,j.a[O].icon]}):t;return Object(n.jsx)(o.c.Provider,{value:v,children:Object(n.jsx)(s.a,{title:f,className:l()("partial-tab-pane",O),isSelected:c,disabled:i,onClick:u,children:b})})})},772:function(e,t,c){"use strict";c.d(t,"a",(function(){return a})),c.d(t,"b",(function(){return i}));var n=c(15),r=c.n(n),a=function(e){return r()(e.match(/regions\.([^.]*)/),1)},i=function(e){return r()(e.match(/vpcs\.([^.]*)/),1)}}}]);
//# sourceMappingURL=22.7b9487ad.chunk.js.map