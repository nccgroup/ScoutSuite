(this.webpackJsonpfrontend=this.webpackJsonpfrontend||[]).push([[12,122],{583:function(e,t,n){"use strict";n.r(t);var r=n(1),i=(n(0),n(55)),o=n(43);t.default=function(){return Object(r.jsxs)(r.Fragment,{children:[Object(r.jsx)(i.c,{label:"ID",valuePath:"id"}),Object(r.jsx)(i.c,{label:"ARN",valuePath:"arn"}),Object(r.jsx)(i.c,{label:"Description",valuePath:"description",renderValue:o.q}),Object(r.jsx)(i.c,{label:"Creation Date",valuePath:"CreateDate",renderValue:o.h}),Object(r.jsx)(i.c,{label:"Status",valuePath:"key_enabled",renderValue:o.c}),Object(r.jsx)(i.c,{label:"Origin",valuePath:"origin",renderValue:o.q}),Object(r.jsx)(i.c,{label:"Key Manager",valuePath:"key_manager",renderValue:o.q}),Object(r.jsx)(i.c,{label:"Rotation",valuePath:"rotation_enabled",renderValue:o.c})]})}},627:function(e,t,n){"use strict";n.r(t);var r=n(1),i=(n(0),n(15)),o=n.n(i),s=n(29),a=n.n(s),l=(n(43),n(55)),c=n(764),p=n(761),u=n(583),h=n(766);t.default=function(e){var t=e.data;if(!t)return null;var n=o()(t,["item","aliases"]),i=o()(t,["item","policy"]);return Object(r.jsxs)(l.a,{data:t,children:[Object(r.jsx)(p.a,{children:Object(r.jsx)(u.default,{})}),Object(r.jsxs)(c.b,{children:[Object(r.jsx)(c.a,{title:"Aliases",disabled:a()(n),children:Object(r.jsx)("ul",{children:n.map((function(e,t){return Object(r.jsx)("li",{children:e.name},t)}))})}),Object(r.jsx)(c.a,{title:"Key Policy",disabled:a()(i),children:Object(r.jsx)(h.a,{policy:i})})]})]})}},761:function(e,t,n){"use strict";var r=n(1);n(0),n(762);t.a=function(e){var t=e.children;return Object(r.jsxs)("div",{className:"informations-wrapper",children:[Object(r.jsx)("h4",{className:"title",children:"Informations"}),t]})}},762:function(e,t,n){},763:function(e,t,n){},764:function(e,t,n){"use strict";n.d(t,"a",(function(){return u})),n.d(t,"b",(function(){return l.b}));var r=n(1),i=n(12),o=n(0),s=n(8),a=n.n(s),l=n(77),c=n(78),p=n(62),u=(n(763),function(e){var t=e.title,n=e.isSelected,s=e.disabled,u=e.onClick,h=e.children,g=Object(o.useState)(""),f=Object(i.a)(g,2),d=f[0],b=f[1],m=d?Object(r.jsxs)(r.Fragment,{children:[t,p.a[d].icon]}):t;return Object(r.jsx)(c.c.Provider,{value:b,children:Object(r.jsx)(l.a,{title:m,className:a()("partial-tab-pane",d),isSelected:n,disabled:s,onClick:u,children:h})})})},765:function(e,t,n){"use strict";var r=n(36),i=n(39);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var o=i(n(0)),s=(0,r(n(40)).default)(o.createElement("path",{d:"M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"}),"ExpandMore");t.default=s},766:function(e,t,n){"use strict";var r=n(1),i=n(12),o=n(0),s=n(8),a=n.n(s),l=n(767),c=n.n(l),p=n(765),u=n.n(p),h=n(769),g=n.n(h),f=n(158),d=n.n(f),b=n(29),m=n.n(b),O=n(78),j=n(226),y=n(43),v=(n(768),function(e){var t=e.name,n=e.policy,s=e.policyPath,l=e.defaultOpen,p=Object(o.useContext)(O.a).path_to_issues.some((function(e){return e.includes(s)}));if(m()(n))return null;var h=Object(r.jsx)("h4",{className:"policy-title",children:t}),f=function(e,t){return Object(r.jsx)(j.a,{value:(n=e,JSON.stringify(n,null,2).replace(/ /gm,"&nbsp;").replace(/\n/gm,"<br/>")),errorPath:t,renderValue:function(e){return Object(y.p)(e)}});var n},b=Object(r.jsxs)("code",{children:["{",Object.entries(n).map((function(e,t){var o=Object(i.a)(e,2),l=o[0],p=o[1];return Object(r.jsxs)("div",{className:a()({inline:"string"===typeof p}),children:['"'.concat(l,'":\xa0'),"Statement"===l?Object(r.jsxs)(r.Fragment,{children:["[",Object(r.jsx)("br",{}),p.map((function(e,t){return Object(r.jsx)(c.a,{trigger:Object(r.jsxs)(r.Fragment,{children:[Object(r.jsx)(u.a,{fontSize:"inherit"}),Object(r.jsx)("span",{children:"{...}"})]}),triggerWhenOpen:Object(r.jsx)(g.a,{fontSize:"inherit"}),transitionTime:1,open:!0,children:f(e,"".concat(s,".Statement.").concat(t))},t)})),"]"]}):Object(r.jsx)(r.Fragment,{children:f(p)}),t<d()(n)-1&&",",Object(r.jsx)("br",{})]},t)})),"}"]});return Object(r.jsx)("div",{className:"policy",children:t?Object(r.jsx)(c.a,{trigger:Object(r.jsxs)(r.Fragment,{children:[h,Object(r.jsx)(u.a,{fontSize:"inherit"})]}),triggerWhenOpen:Object(r.jsxs)(r.Fragment,{children:[h,Object(r.jsx)(g.a,{fontSize:"inherit"})]}),transitionTime:1,open:l||p,children:b}):b})});v.defaultProps={defaultOpen:!1},t.a=v},767:function(e,t,n){var r;e.exports=(r=n(0),function(e){var t={};function n(r){if(t[r])return t[r].exports;var i=t[r]={i:r,l:!1,exports:{}};return e[r].call(i.exports,i,i.exports,n),i.l=!0,i.exports}return n.m=e,n.c=t,n.d=function(e,t,r){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(n.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var i in e)n.d(r,i,function(t){return e[t]}.bind(null,i));return r},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=4)}([function(e,t,n){e.exports=n(2)()},function(e,t){e.exports=r},function(e,t,n){"use strict";var r=n(3);function i(){}function o(){}o.resetWarningCache=i,e.exports=function(){function e(e,t,n,i,o,s){if(s!==r){var a=new Error("Calling PropTypes validators directly is not supported by the `prop-types` package. Use PropTypes.checkPropTypes() to call them. Read more at http://fb.me/use-check-prop-types");throw a.name="Invariant Violation",a}}function t(){return e}e.isRequired=e;var n={array:e,bool:e,func:e,number:e,object:e,string:e,symbol:e,any:e,arrayOf:t,element:e,elementType:e,instanceOf:t,node:e,objectOf:t,oneOf:t,oneOfType:t,shape:t,exact:t,checkPropTypes:o,resetWarningCache:i};return n.PropTypes=n,n}},function(e,t,n){"use strict";e.exports="SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED"},function(e,t,n){"use strict";n.r(t);var r=n(1),i=n.n(r),o=n(0),s=n.n(o),a=function(e){return 0!==e};function l(e){return(l="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function c(){return(c=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}function p(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function u(e,t){return(u=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function h(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=d(e);if(t){var i=d(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return g(this,n)}}function g(e,t){return!t||"object"!==l(t)&&"function"!=typeof t?f(e):t}function f(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function d(e){return(d=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function b(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var m=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&u(e,t)}(s,e);var t,n,r,o=h(s);function s(e){var t;return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,s),b(f(t=o.call(this,e)),"continueOpenCollapsible",(function(){var e=f(t).innerRef;t.setState({height:e.scrollHeight,transition:"height ".concat(t.props.transitionTime,"ms ").concat(t.props.easing),isClosed:!1,hasBeenOpened:!0,inTransition:a(e.scrollHeight),shouldOpenOnNextCycle:!1})})),b(f(t),"handleTriggerClick",(function(e){t.props.triggerDisabled||t.state.inTransition||(e.preventDefault(),t.props.handleTriggerClick?t.props.handleTriggerClick(t.props.accordionPosition):!0===t.state.isClosed?(t.openCollapsible(),t.props.onOpening(),t.props.onTriggerOpening()):(t.closeCollapsible(),t.props.onClosing(),t.props.onTriggerClosing()))})),b(f(t),"handleTransitionEnd",(function(e){e.target===t.innerRef&&(t.state.isClosed?(t.setState({inTransition:!1}),t.props.onClose()):(t.setState({height:"auto",overflow:t.props.overflowWhenOpen,inTransition:!1}),t.props.onOpen()))})),b(f(t),"setInnerRef",(function(e){return t.innerRef=e})),t.timeout=void 0,e.open?t.state={isClosed:!1,shouldSwitchAutoOnNextCycle:!1,height:"auto",transition:"none",hasBeenOpened:!0,overflow:e.overflowWhenOpen,inTransition:!1}:t.state={isClosed:!0,shouldSwitchAutoOnNextCycle:!1,height:0,transition:"height ".concat(e.transitionTime,"ms ").concat(e.easing),hasBeenOpened:!1,overflow:"hidden",inTransition:!1},t}return t=s,(n=[{key:"componentDidUpdate",value:function(e,t){var n=this;this.state.shouldOpenOnNextCycle&&this.continueOpenCollapsible(),"auto"!==t.height&&0!==t.height||!0!==this.state.shouldSwitchAutoOnNextCycle||(window.clearTimeout(this.timeout),this.timeout=window.setTimeout((function(){n.setState({height:0,overflow:"hidden",isClosed:!0,shouldSwitchAutoOnNextCycle:!1})}),50)),e.open!==this.props.open&&(!0===this.props.open?(this.openCollapsible(),this.props.onOpening()):(this.closeCollapsible(),this.props.onClosing()))}},{key:"componentWillUnmount",value:function(){window.clearTimeout(this.timeout)}},{key:"closeCollapsible",value:function(){var e=this.innerRef;this.setState({shouldSwitchAutoOnNextCycle:!0,height:e.scrollHeight,transition:"height ".concat(this.props.transitionCloseTime?this.props.transitionCloseTime:this.props.transitionTime,"ms ").concat(this.props.easing),inTransition:a(e.scrollHeight)})}},{key:"openCollapsible",value:function(){this.setState({inTransition:a(this.innerRef.scrollHeight),shouldOpenOnNextCycle:!0})}},{key:"renderNonClickableTriggerElement",value:function(){return this.props.triggerSibling&&"string"==typeof this.props.triggerSibling?i.a.createElement("span",{className:"".concat(this.props.classParentString,"__trigger-sibling")},this.props.triggerSibling):this.props.triggerSibling&&"function"==typeof this.props.triggerSibling?this.props.triggerSibling():this.props.triggerSibling?i.a.createElement(this.props.triggerSibling,null):null}},{key:"render",value:function(){var e=this,t={height:this.state.height,WebkitTransition:this.state.transition,msTransition:this.state.transition,transition:this.state.transition,overflow:this.state.overflow},n=this.state.isClosed?"is-closed":"is-open",r=this.props.triggerDisabled?"is-disabled":"",o=!1===this.state.isClosed&&void 0!==this.props.triggerWhenOpen?this.props.triggerWhenOpen:this.props.trigger,s=this.props.contentContainerTagName,a=this.props.triggerTagName,l=this.props.lazyRender&&!this.state.hasBeenOpened&&this.state.isClosed&&!this.state.inTransition?null:this.props.children,p="".concat(this.props.classParentString,"__trigger ").concat(n," ").concat(r," ").concat(this.state.isClosed?this.props.triggerClassName:this.props.triggerOpenedClassName),u="".concat(this.props.classParentString," ").concat(this.state.isClosed?this.props.className:this.props.openedClassName),h="".concat(this.props.classParentString,"__contentOuter ").concat(this.props.contentOuterClassName),g="".concat(this.props.classParentString,"__contentInner ").concat(this.props.contentInnerClassName);return i.a.createElement(s,c({className:u.trim()},this.props.containerElementProps),i.a.createElement(a,c({className:p.trim(),onClick:this.handleTriggerClick,style:this.props.triggerStyle&&this.props.triggerStyle,onKeyPress:function(t){var n=t.key;(" "===n&&"button"!==e.props.triggerTagName.toLowerCase()||"Enter"===n)&&e.handleTriggerClick(t)},tabIndex:this.props.tabIndex&&this.props.tabIndex},this.props.triggerElementProps),o),this.renderNonClickableTriggerElement(),i.a.createElement("div",{className:h.trim(),style:t,onTransitionEnd:this.handleTransitionEnd,ref:this.setInnerRef,hidden:this.props.contentHiddenWhenClosed&&this.state.isClosed&&!this.state.inTransition},i.a.createElement("div",{className:g.trim()},l)))}}])&&p(t.prototype,n),r&&p(t,r),s}(r.Component);m.propTypes={transitionTime:s.a.number,transitionCloseTime:s.a.number,triggerTagName:s.a.string,easing:s.a.string,open:s.a.bool,containerElementProps:s.a.object,triggerElementProps:s.a.object,classParentString:s.a.string,openedClassName:s.a.string,triggerStyle:s.a.object,triggerClassName:s.a.string,triggerOpenedClassName:s.a.string,contentOuterClassName:s.a.string,contentInnerClassName:s.a.string,accordionPosition:s.a.oneOfType([s.a.string,s.a.number]),handleTriggerClick:s.a.func,onOpen:s.a.func,onClose:s.a.func,onOpening:s.a.func,onClosing:s.a.func,onTriggerOpening:s.a.func,onTriggerClosing:s.a.func,trigger:s.a.oneOfType([s.a.string,s.a.element]),triggerWhenOpen:s.a.oneOfType([s.a.string,s.a.element]),triggerDisabled:s.a.bool,lazyRender:s.a.bool,overflowWhenOpen:s.a.oneOf(["hidden","visible","auto","scroll","inherit","initial","unset"]),contentHiddenWhenClosed:s.a.bool,triggerSibling:s.a.oneOfType([s.a.element,s.a.func]),tabIndex:s.a.number,contentContainerTagName:s.a.string},m.defaultProps={transitionTime:400,transitionCloseTime:null,triggerTagName:"span",easing:"linear",open:!1,classParentString:"Collapsible",triggerDisabled:!1,lazyRender:!1,overflowWhenOpen:"hidden",contentHiddenWhenClosed:!1,openedClassName:"",triggerStyle:null,triggerClassName:"",triggerOpenedClassName:"",contentOuterClassName:"",contentInnerClassName:"",className:"",triggerSibling:null,onOpen:function(){},onClose:function(){},onOpening:function(){},onClosing:function(){},onTriggerOpening:function(){},onTriggerClosing:function(){},tabIndex:null,contentContainerTagName:"div"},t.default=m}]))},768:function(e,t,n){},769:function(e,t,n){"use strict";var r=n(36),i=n(39);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var o=i(n(0)),s=(0,r(n(40)).default)(o.createElement("path",{d:"M12 8l-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z"}),"ExpandLess");t.default=s}}]);
//# sourceMappingURL=12.5701f422.chunk.js.map