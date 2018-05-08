<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>Centara GP | Dashboard</title>
  <!-- Tell the browser to be responsive to screen width -->
  <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
  <!-- Bootstrap 3.3.7 -->
  <link rel="stylesheet" href="/static/bower_components/bootstrap/dist/css/bootstrap.min.css">
  <!-- Font Awesome -->
  <link rel="stylesheet" href="/static/bower_components/font-awesome/css/font-awesome.min.css">
  <!-- Ionicons -->
  <link rel="stylesheet" href="/static/bower_components/Ionicons/css/ionicons.min.css">
  <!-- jvectormap -->
  <link rel="stylesheet" href="/static/bower_components/jvectormap/jquery-jvectormap.css">
  <!-- Theme style -->
  <link rel="stylesheet" href="/static/dist/css/AdminLTE.min.css">
   <!-- Bootstrap time Picker -->
  <link rel="stylesheet" href="/static/plugins/timepicker/bootstrap-timepicker.min.css">
   <!-- iCheck for checkboxes and radio inputs -->
  <link rel="stylesheet" href="/static/plugins/iCheck/all.css">
  <!-- AdminLTE Skins. Choose a skin from the css/skins
       folder instead of downloading all of them to reduce the load. -->
  <link rel="stylesheet" href="/static/dist/css/skins/_all-skins.min.css">
  <!-- DataTables -->
  <link rel="stylesheet" href="/static/bower_components/datatables.net-bs/css/dataTables.bootstrap.min.css">
  <!-- Select2 -->
  <link rel="stylesheet" href="/static/bower_components/select2/dist/css/select2.min.css">
   <link rel="stylesheet" href="/static/dist/css/css/style.css">
  <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
  <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
  <!--[if lt IE 9]>
  <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
  <![endif]-->

<style type="text/css">
.row > .hAlign {
    display:flex;
    flex: 0 0 100%;
    max-width: 100%
}
.row > .pCreate {
    display:flex;
    flex: 0 0 100%;
    max-width: 70%
}
.row > .profile {
    display:flex;
    flex: 0 0 100%;
    max-width: 70%
}
.row > .drugProfile {
    display:flex;
    flex: 0 0 100%;
    max-width: 55%
}
.row > .drugCreate {
    display:flex;
    flex: 0 0 100%;
    max-width: 35%
}

.flex-nowrap {
    -webkit-flex-wrap: nowrap!important;
    -ms-flex-wrap: nowrap!important;
    flex-wrap: nowrap!important;
}
.flex-row {
    display:flex;
	overflow-y:hidden;
	height:88vh;
    -webkit-box-orient: horizontal!important;
    -webkit-box-direction: normal!important;
    -webkit-flex-direction: row!important;
    -ms-flex-direction: row!important;
    flex-direction: row!important;
}

/*
 *  STYLE 1
 */

#style-1::-webkit-scrollbar-track
{
	-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
	border-radius: 10px;
	background-color: #F5F5F5;
}

#style-1::-webkit-scrollbar
{
	width: 4px;
	background-color: grey;
}

#style-1::-webkit-scrollbar-thumb
{
	border-radius: 10px;
	-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);
	background-color: #555;
}
/* 
 *  Admin Tables
 */

.table-group{
  width:65%;
  margin-top: 35px;
}
.table-group > thead > tr{
  background-color: #222d32;
  color: white;
}
.table-group > thead > tr > td > span{
  margin:15px;
  line-height: 2.4em;
  font-size: 16px;
  font-weight: 600;
  font-family: sans-serif;
}
.table-group > tbody > tr{
  border-bottom: solid 1px rgba(187, 178, 178, 0.62);
  color:#3c8dbc;
  background-color: #eaeaea;
}
.table-group > tbody > tr > td > div{
  margin:8px 15px;
  font-size: 14px;
  font-weight: 600;
  font-family: sans-serif;
}
.modify{
  float:right;
}
.modify:hover{
  cursor: pointer;
}
.pmodify{
  float:right;
  color:black;
  font-weight: 600;
}
.pmodify:hover{
  color:white;
}
.add{
  float:right;
  margin-right: 25px;
}
.add:hover{
  cursor:pointer;
}
.title:hover{
  cursor:pointer;
}

.btn-flat:hover{
  background-color: #3c8dbc;
  color:white;
}

</style>

  <!-- Google Font -->
  <link rel="stylesheet"
        href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700,300italic,400italic,600italic">
</head>
<body class="hold-transition skin-blue sidebar-mini sidebar-collapse" style="overflow:hidden; height: 100vh">
<div class="wrapper" style="height:100vh background-color:transparent;">

  <header class="main-header">

    <!-- Logo -->
    <a href="index2.html" class="logo">
      <!-- mini logo for sidebar mini 50x50 pixels -->
      <span class="logo-mini"><b>C</b>HP</span>
      <!-- logo for regular state and mobile devices -->
      <span class="logo-lg"><b>Centra</b>HP</span>
    </a>

    <!-- Header Navbar: style can be found in header.less -->
    <nav class="navbar navbar-static-top">
      <!-- Sidebar toggle button-->
      <a href="#" class="sidebar-toggle" data-toggle="push-menu" role="button">
        <span class="sr-only">Toggle navigation</span>
      </a>
      <!-- Navbar Right Menu -->
      <div class="navbar-custom-menu">
        <ul class="nav navbar-nav">
          <!-- User Account: style can be found in dropdown.less -->
          <li class="dropdown user user-menu">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
              <img src="/static/dist/img/user2-160x160.jpg" class="user-image" alt="User Image">
              <span class="hidden-xs">logout</span>
            </a>
          </li> 
        </ul>
      </div>

    </nav>
  </header>
  <!-- Left side column. contains the logo and sidebar -->
  <aside class="main-sidebar" style="background-color: #222d32;">
    <!-- sidebar: style can be found in sidebar.less -->
    <section class="sidebar">
      <!-- Sidebar user panel -->
      <div class="user-panel">
        <div class="pull-left image">
          <img src="/static/dist/img/user2-160x160.jpg" class="img-circle" alt="User Image">
        </div>
        <div class="pull-left info" style="">
          <p>{{data}}</p>
        </div>
      </div>
      <!-- /.search form -->
      <!-- sidebar menu: : style can be found in sidebar.less -->
      <ul class="sidebar-menu" data-widget="tree">
        
      </ul>
    </section>
    <!-- /.sidebar -->
  </aside>

  <!-- Content Wrapper. Contains page content -->
  <div class="content-wrapper" style="height: 95vh;">

    <!-- Main content -->
    <div class=" content container-fluid" style="padding:0px;">
      <div class="row flex-row flex-nowrap" style="margin:0px;">     
       <div class="col-md-12 hAlign" style="padding: 0px;" id="main">
        <div class="box" style="height:88vh;border-right:solid 1px grey; ">
         
          <!-- /.box-header -->
          <div class="box-body scrollbar" id="style-1" style="height:88vh; overflow-y:auto;overflow-x:hidden; ">
            <div class="container">
              <h2>Site administration</h2>
              <!-- data groups -->
              <div>
                <!-- table-group-1 -->
                <table class="table-group">
                  <thead>
                    <tr>
                      <td><span> AUTHENTICATION AND AUTHORIZATION </span></td>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>
                        <div>
                          <span class="title" id="users">Users</span>
                          <span class="add" id="addUser"><i class="fa  fa-plus"  style="margin-right: 10px;color: green;"></i>Add</span>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <!-- !group-1 -->
                <!-- group-2 -->
                <table class="table-group">
                  <thead>
                    <tr>
                      <td><span>DATA TABLES </span></td>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>
                        <div>
                          <span class="title" id="patients">Patients</span>
                          <span class="add" id="patientsAdd"><i class="fa  fa-plus"  style="margin-right: 10px; color: green;"></i>Add</span>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <div>
                          <span class="title" id="drugs">Drugs</span>
                          <span class="add" id="addDrug"><i class="fa  fa-plus"  style="margin-right: 10px; color: green;"></i>Add</span>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <div>
                          <span class="title" id="medConditions">Medical Conditions</span>
                          <span class="add" id="medConditionsAdd"><i class="fa  fa-plus"  style="margin-right: 10px; color: green;"></i>Add</span>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <div>
                          <span class="title" id="radiology">Radiology Tests</span>
                          <span class="add" id="radiologyAdd"><i class="fa  fa-plus"  style="margin-right: 10px; color: green;"></i>Add</span>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <!-- !group-2 -->
                 <!-- group-3 -->
                <table class="table-group">
                  <thead>
                    <tr>
                      <td><span> INSTITUTION</span></td>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>
                        <div>
                          <span class="title">Marina</span>
                          <span class="add" id="institutionAdd"><i class="fa  fa-plus"  style="margin-right: 10px;color: green;"></i>Add</span>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <!-- !group-3 -->
                <!-- group-4 -->
                <table class="table-group">
                  <thead>
                    <tr>
                      <td><span> LOGS </span></td>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>
                        <div>
                          <span class="title">Clinical record logs</span>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <div>
                          <span class="title">Radiology logs</span>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <div>
                          <span class="title">System Error logs</span>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <!-- !group-4 -->
              </div>
              <!-- !data groups -->
            </div>
            <!-- container -->
          </div>
          <!-- !box-header -->
        </div>
        <!-- box -->
       </div>
       <!-- col -->
      </div>	
      <!-- flex-row -->
    </div>      
    <!-- /.content -->
  </div>
  <!-- /.content-wrapper -->

  <footer class="main-footer">
    <div class="pull-right hidden-xs">
      <b>Version</b> 2.4.0
    </div>
  </footer>

</div>
<!-- ./wrapper -->

<!-- jQuery 3 -->
<script src="/static/bower_components/jquery/dist/jquery.min.js" charset="utf-8"></script>
<!-- Bootstrap 3.3.7 -->
<script src="/static/bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
<!-- FastClick -->
<script src="/static/bower_components/fastclick/lib/fastclick.js"></script>
<!-- AdminLTE App -->
<script src="/static/dist/js/adminlte.min.js"></script>
<!-- Sparkline -->
<script src="/static/bower_components/jquery-sparkline/dist/jquery.sparkline.min.js"></script>
<!-- Select2 -->
<script src="/static/bower_components/select2/dist/js/select2.full.min.js"></script>
<!-- InputMask -->
<script src="/static/plugins/input-mask/jquery.inputmask.js"></script>
<script src="/static/plugins/input-mask/jquery.inputmask.date.extensions.js"></script>
<script src="/static/plugins/input-mask/jquery.inputmask.extensions.js"></script>
<script src="/static/dist/js/app.js"></script>
<script src="/static/plugins/jQuery_Form_Validator_files/jquery.form-validator.min.js"></script>

<!-- DataTables -->
<script src="/static/bower_components/datatables.net/js/jquery.dataTables.min.js"></script>
<script src="/static/bower_components/datatables.net-bs/js/dataTables.bootstrap.min.js"></script>

<!-- SlimScroll -->
<script src="/static/bower_components/jquery-slimscroll/jquery.slimscroll.min.js"></script>

<!-- iCheck 1.0.1 -->
<script src="/static/plugins/iCheck/icheck.min.js"></script>
<!-- bootstrap datepicker -->
<script src="/static/bower_components/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js"></script>


<!-- Page script -->
<script>
$(document).ready(function(e){
  $(function () {
    $('#example1').DataTable({
      'paging'      : false,
      'lengthChange': false,
      'searching'   : true,
      'ordering'    : false,
      'info'        : true,
      'autoWidth'   : false,
    "pageLength"  : 500
    });
    $('#example3').DataTable({
    'paging'      : false,
      'lengthChange': false,
      'searching'   : true,
      'ordering'    : false,
      'info'        : true,
      'autoWidth'   : false,
    "pageLength"  : 500
  });
  $('#example4').DataTable({
    'paging'      : false,
      'lengthChange': false,
      'searching'   : true,
      'ordering'    : false,
      'info'        : true,
      'autoWidth'   : false,
    "pageLength"  : 500
  });
  })

  $(function () {
    //Initialize Select2 Elements
    $('.select2').select2()

    //iCheck for checkbox and radio inputs
    $('input[type="checkbox"].minimal, input[type="radio"].minimal').iCheck({
      checkboxClass: 'icheckbox_minimal-blue',
      radioClass   : 'iradio_minimal-blue'
    })
    //Red color scheme for iCheck
    $('input[type="checkbox"].minimal-red, input[type="radio"].minimal-red').iCheck({
      checkboxClass: 'icheckbox_minimal-red',
      radioClass   : 'iradio_minimal-red'
    })
    //Flat red color scheme for iCheck
    $('input[type="checkbox"].flat-red, input[type="radio"].flat-red').iCheck({
      checkboxClass: 'icheckbox_flat-green',
      radioClass   : 'iradio_flat-green'
    })
  });
});
</script>
</body>
</html>
