import{a as A,b as U}from"./chunk-LD5PMWLX.js";import{Ba as x,Ca as G,Da as P,Ea as k,Ha as V,Ia as j,ca as S,ga as w,ja as y,la as p,na as M,oa as E,pa as _,ra as d,sa as C,ua as N,va as D,xa as I,ya as g}from"./chunk-R3YEXRHJ.js";import{Cb as i,Db as e,Eb as n,Lb as h,Vb as r,Xb as F,Za as s,_a as u,_b as b,ka as v,tb as f}from"./chunk-56V3A5FK.js";var X=(()=>{let a=class a{constructor(t,o){this._appDataService=t,this._securityService=o,this.mainForm=this._constructForm()}ngOnInit(){this._appDataService.currentUser$.subscribe(t=>{this.member=t,this.mainForm.patchValue({name:this.member?.name,email:this.member?.email}),this.mainForm.controls.email.disable()})}_constructForm(){return new _({name:new d(null,[p.required]),email:new d(null,[p.required,p.email]),password:new d(null)})}update(){let t=this._preparePayload();this._securityService.updateCurrentUser(t).subscribe(()=>{this._appDataService.initializeUser(),this.mainForm.markAsPristine()})}_preparePayload(){let t={};return this.mainForm.controls.name.dirty&&(t.name=this.mainForm.controls.name.value),this.mainForm.controls.password.value&&(t.password=this.mainForm.controls.password.value),t}};a.\u0275fac=function(o){return new(o||a)(u(j),u(V))},a.\u0275cmp=v({type:a,selectors:[["app-member-profile"]],standalone:!0,features:[b],decls:26,vars:3,consts:[[1,"text-align-center"],[1,"p-4","w-50"],[3,"formGroup"],[1,"w-100","mt-2"],["matInput","","placeholder","Name","formControlName","name"],["matInput","","placeholder","Email","formControlName","email"],["matInput","","type","password","placeholder","Enter new password or leave empty","formControlName","password"],["mat-flat-button","","color","primary","aria-label","Add row",1,"mt-2",3,"click","disabled"]],template:function(o,m){if(o&1&&(i(0,"section",0)(1,"h1"),r(2,"Profile"),e(),i(3,"p"),r(4),e()(),n(5,"mat-divider"),i(6,"section",1)(7,"h3"),r(8,"Update profile"),e(),i(9,"form",2)(10,"mat-form-field",3)(11,"mat-label"),r(12,"Name"),e(),n(13,"input",4),e(),i(14,"mat-form-field",3)(15,"mat-label"),r(16,"Email"),e(),n(17,"input",5),e(),i(18,"mat-form-field",3)(19,"mat-label"),r(20,"New password"),e(),n(21,"input",6),e(),i(22,"button",7),h("click",function(){return m.update()}),i(23,"mat-icon"),r(24,"save"),e(),r(25," Save "),e()()()),o&2){let l;s(4),F("Balance: ",(l=m.member==null?null:m.member.balance)!==null&&l!==void 0?l:0,""),s(5),f("formGroup",m.mainForm),s(13),f("disabled",!m.mainForm.dirty||!m.mainForm.valid)}},dependencies:[U,A,I,C,y,M,E,N,D,G,x,g,k,P,S,w]});let c=a;return c})();export{X as MemberProfileComponent};
