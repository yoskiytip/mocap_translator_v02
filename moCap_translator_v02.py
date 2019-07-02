import ast, sys, math
from PySide2 import QtWidgets, QtGui, QtCore
from maya import cmds


class MoCap_UI(QtWidgets.QDialog):
    def __init__(self):
        super(MoCap_UI, self).__init__()

        self.form_lb_width = 40
        self.form_fld_width = 150
        self.form_row_width = self.form_lb_width + self.form_fld_width + 20

        # Mocap joint fields object names list
        self.body_joints_controls_lines_list = []
        self.face_joints_controls_lines_list = []

        # Init
        self.initGUI()
        self.init_signals()

    def initGUI(self):
        self.setWindowTitle('Human Generator')
        self.setGeometry(300, 300, 600, 600)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        # self.setFixedWidth(600)
        # Body Mocap Widget
        self.init_body_mocap_widget()
        # Face Mocap Widget
        self.init_face_mocap_widget()
        # Tabs
        self.tabs_widget = QtWidgets.QTabWidget()
        self.layout().addWidget(self.tabs_widget)
        self.tabs_widget.addTab(self.body_mocap_widget, 'Body')
        self.tabs_widget.addTab(self.face_mocap_widget, 'Face')

    def init_body_mocap_widget(self):
        self.body_mocap_widget = Custom_Layout_Widget('vert', (6, 10, 6, 6), 6, 'top')
        # Header Widget
        header_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 6, 'left', height=20)
        self.body_mocap_widget.layout().addWidget(header_widget)
        # Root to Names button
        self.root_to_names_btn = QtWidgets.QPushButton('Root -> Names')
        self.root_to_names_btn.setFixedWidth(100)
        header_widget.layout().addWidget(self.root_to_names_btn)
        #
        Splitter_Vert(header_widget, 1)
        # Template
        template_lb = QtWidgets.QLabel('Template:')
        header_widget.layout().addWidget(template_lb)
        #
        self.body_template_le = QtWidgets.QLineEdit()
        self.body_template_le.setFixedWidth(300)
        header_widget.layout().addWidget(self.body_template_le)
        #
        self.body_save_template_btn = QtWidgets.QPushButton('Save')
        self.body_save_template_btn.setFixedWidth(40)
        self.body_load_template_btn = QtWidgets.QPushButton('Load')
        self.body_load_template_btn.setFixedWidth(40)
        header_widget.layout().addWidget(self.body_save_template_btn)
        header_widget.layout().addWidget(self.body_load_template_btn)
        #
        Splitter_Hor(self.body_mocap_widget, 6)
        # Joints
        joints_header_lb = QtWidgets.QLabel('   Mocap Joints                         '
                                            'Control Objects                       '
                                            'Constraint Options                          '
                                            'ID')
        joints_header_lb.setFixedHeight(18)
        self.body_mocap_widget.layout().addWidget(joints_header_lb)
        #
        self.body_joints_widget = Custom_Layout_Widget('vert', (4, 4, 4, 4), 6, 'top')
        body_scrollArea = QtWidgets.QScrollArea()
        self.body_mocap_widget.layout().addWidget(body_scrollArea)
        body_scrollArea.setWidgetResizable(True)
        body_scrollArea.setWidget(self.body_joints_widget)
        #
        # Add joint line button
        body_add_line_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 0, 'top', height=20)
        self.body_add_line_btn = QtWidgets.QPushButton('Add Line')
        self.body_add_line_btn.setFixedWidth(240)
        body_add_line_widget.layout().addWidget(QtWidgets.QFrame())
        body_add_line_widget.layout().addWidget(self.body_add_line_btn)
        body_add_line_widget.layout().addWidget(QtWidgets.QFrame())
        self.body_mocap_widget.layout().addWidget(body_add_line_widget)
        #
        Splitter_Hor(self.body_mocap_widget, 6)
        # Init Pose --------------------------------------------------------------------------------------
        body_init_pose_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 6, 'left', height=20)
        self.body_mocap_widget.layout().addWidget(body_init_pose_widget)
        #
        self.body_create_init_pose_btn = QtWidgets.QPushButton('Create Init Pose')
        self.body_create_init_pose_btn.setFixedWidth(120)
        body_init_pose_widget.layout().addWidget(self.body_create_init_pose_btn)
        Splitter_Vert(body_init_pose_widget, 6)
        #
        body_init_pose_lb = QtWidgets.QLabel('Init Frame:')
        body_init_pose_lb.setFixedWidth(60)
        body_init_pose_widget.layout().addWidget(body_init_pose_lb)
        #
        self.body_init_pose_frame_le = QtWidgets.QLineEdit('-100')
        self.body_init_pose_frame_le.setFixedWidth(40)
        body_init_pose_widget.layout().addWidget(self.body_init_pose_frame_le)
        #
        Splitter_Vert(body_init_pose_widget, 6)
        #
        self.body_save_init_pose_btn = QtWidgets.QPushButton('Save Init Pose')
        self.body_save_init_pose_btn.setFixedWidth(100)
        body_init_pose_widget.layout().addWidget(self.body_save_init_pose_btn)
        #
        self.body_load_init_pose_btn = QtWidgets.QPushButton('Load Init Pose')
        self.body_load_init_pose_btn.setFixedWidth(100)
        body_init_pose_widget.layout().addWidget(self.body_load_init_pose_btn)
        #
        Splitter_Hor(self.body_mocap_widget, 6)
        # Mirror joint --------------------------------------------------------------------------------------
        body_mirror_joint_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 6, 'left', height=20)
        self.body_mocap_widget.layout().addWidget(body_mirror_joint_widget)
        #
        self.body_mirror_joint_btn = QtWidgets.QPushButton('Mirror Joint')
        self.body_mirror_joint_btn.setFixedWidth(120)
        body_mirror_joint_widget.layout().addWidget(self.body_mirror_joint_btn)
        Splitter_Vert(body_mirror_joint_widget, 6)
        #
        body_mirror_left_ID_lb = QtWidgets.QLabel('Left Prefix:')
        body_mirror_left_ID_lb.setFixedWidth(60)
        body_mirror_joint_widget.layout().addWidget(body_mirror_left_ID_lb)
        #
        self.body_mirror_left_ID_le = QtWidgets.QLineEdit('_L')
        self.body_mirror_left_ID_le.setFixedWidth(40)
        body_mirror_joint_widget.layout().addWidget(self.body_mirror_left_ID_le)
        #
        Splitter_Vert(body_mirror_joint_widget, 8)
        #
        body_mirror_right_ID_lb = QtWidgets.QLabel('Right Prefix:')
        body_mirror_right_ID_lb.setFixedWidth(60)
        body_mirror_joint_widget.layout().addWidget(body_mirror_right_ID_lb)
        #
        self.body_mirror_right_ID_le = QtWidgets.QLineEdit('_R')
        self.body_mirror_right_ID_le.setFixedWidth(40)
        body_mirror_joint_widget.layout().addWidget(self.body_mirror_right_ID_le)

        #
        Splitter_Hor(self.body_mocap_widget, 6)
        # Bind controls --------------------------------------------------------------------------------------
        body_bind_controls_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 6, 'left', height=20)
        self.body_mocap_widget.layout().addWidget(body_bind_controls_widget)
        #
        self.body_bind_controls_btn = QtWidgets.QPushButton('Bind Controls')
        self.body_bind_controls_btn.setFixedWidth(120)
        body_bind_controls_widget.layout().addWidget(self.body_bind_controls_btn)
        Splitter_Vert(body_bind_controls_widget, 6)

        #
        Splitter_Hor(self.body_mocap_widget, 6)
        # Bake animation --------------------------------------------------------------------------------------
        body_bake_anim_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 6, 'left', height=20)
        self.body_mocap_widget.layout().addWidget(body_bake_anim_widget)
        #
        self.body_bake_anim_btn = QtWidgets.QPushButton('Bake Animation')
        self.body_bake_anim_btn.setFixedWidth(120)
        body_bake_anim_widget.layout().addWidget(self.body_bake_anim_btn)
        Splitter_Vert(body_bake_anim_widget, 6)
        #
        body_start_bake_lb = QtWidgets.QLabel('Start Frame:')
        body_start_bake_lb.setFixedWidth(60)
        body_bake_anim_widget.layout().addWidget(body_start_bake_lb)
        #
        self.body_start_bake_le = QtWidgets.QLineEdit('1')
        self.body_start_bake_le.setFixedWidth(40)
        body_bake_anim_widget.layout().addWidget(self.body_start_bake_le)
        #
        Splitter_Vert(body_bake_anim_widget, 8)
        #
        body_end_bake_lb = QtWidgets.QLabel('End Frame:')
        body_end_bake_lb.setFixedWidth(60)
        body_bake_anim_widget.layout().addWidget(body_end_bake_lb)
        #
        self.body_end_bake_le = QtWidgets.QLineEdit('120')
        self.body_end_bake_le.setFixedWidth(40)
        body_bake_anim_widget.layout().addWidget(self.body_end_bake_le)
        #
        Splitter_Vert(body_bake_anim_widget, 8)
        #
        body_bake_interval_lb = QtWidgets.QLabel('Interval:')
        body_bake_interval_lb.setFixedWidth(60)
        body_bake_anim_widget.layout().addWidget(body_bake_interval_lb)
        #
        self.body_bake_interval_le = QtWidgets.QLineEdit('1')
        self.body_bake_interval_le.setFixedWidth(40)
        body_bake_anim_widget.layout().addWidget(self.body_bake_interval_le)

    def init_face_mocap_widget(self):
        self.face_mocap_widget = Custom_Layout_Widget('vert', (6, 10, 6, 6), 8, 'top')
        # Header Widget
        face_header_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 6, 'left', height=20)
        self.face_mocap_widget.layout().addWidget(face_header_widget)
        # Root to Names button
        self.load_selection_btn = QtWidgets.QPushButton('Load Selection')
        self.load_selection_btn.setFixedWidth(100)
        face_header_widget.layout().addWidget(self.load_selection_btn)
        #
        Splitter_Vert(face_header_widget, 1)
        # Template
        template_lb = QtWidgets.QLabel('Template:')
        template_lb.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        face_header_widget.layout().addWidget(template_lb)
        #
        self.face_template_le = QtWidgets.QLineEdit()
        face_header_widget.layout().addWidget(self.face_template_le)
        #
        self.face_save_template_btn = QtWidgets.QPushButton('Save')
        self.face_save_template_btn.setFixedWidth(40)
        self.face_load_template_btn = QtWidgets.QPushButton('Load')
        self.face_load_template_btn.setFixedWidth(40)
        face_header_widget.layout().addWidget(self.face_save_template_btn)
        face_header_widget.layout().addWidget(self.face_load_template_btn)
        #
        Splitter_Hor(self.face_mocap_widget, 6)
        # Detect Reference Points --------------------------------------------------------------------------------------
        face_points_detection_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 6, 'left', height=20)
        self.face_mocap_widget.layout().addWidget(face_points_detection_widget)
        points_detection_lb = QtWidgets.QLabel('Target Objects Prefix:')
        points_detection_lb.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        face_points_detection_widget.layout().addWidget(points_detection_lb)
        #
        self.target_objects_prefix_le = QtWidgets.QLineEdit()
        self.target_objects_prefix_le.setFixedWidth(60)
        face_points_detection_widget.layout().addWidget(self.target_objects_prefix_le)
        Splitter_Vert(face_points_detection_widget, 4)
        #
        max_target_number_lb = QtWidgets.QLabel('Max Points:')
        face_points_detection_widget.layout().addWidget(max_target_number_lb)
        face_points_detection_widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        #
        self.max_target_number_le = QtWidgets.QLineEdit('2')
        self.max_target_number_le.setFixedWidth(40)
        face_points_detection_widget.layout().addWidget(self.max_target_number_le)
        Splitter_Vert(face_points_detection_widget, 4)
        #
        self.find_target_objects_btn = QtWidgets.QPushButton('Find Target Objects')
        face_points_detection_widget.layout().addWidget(self.find_target_objects_btn)
        Splitter_Vert(face_points_detection_widget, 4)
        #
        self.create_ref_objects_btn = QtWidgets.QPushButton('Create Ref Objs')
        face_points_detection_widget.layout().addWidget(self.create_ref_objects_btn)
        #
        Splitter_Hor(self.face_mocap_widget, 6)
        # Controls -----------------------------------------------------------------------------------------------------
        controls_header_lb = QtWidgets.QLabel('   Face Control                          '
                                              'Source Object                       '
                                              'Mode               '
                                              'Mult      '
                                              'Axes            '
                                              'Mapping  ')
        controls_header_lb.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.face_mocap_widget.layout().addWidget(controls_header_lb)
        #
        self.face_controls_widget = Custom_Layout_Widget('vert', (4, 4, 4, 4), 6, 'top')
        face_scrollArea = QtWidgets.QScrollArea()
        self.face_mocap_widget.layout().addWidget(face_scrollArea)
        face_scrollArea.setWidgetResizable(True)
        face_scrollArea.setWidget(self.face_controls_widget)
        # Add joint line button ----------------------------------------------------------------------------------------
        face_add_line_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 0, 'top', height=20)
        self.face_bulk_mod_btn = QtWidgets.QPushButton('Bulk Modify Lines')
        self.face_bulk_mod_btn.setFixedWidth(120)
        #
        self.face_add_line_btn = QtWidgets.QPushButton('Add Line')
        self.face_add_line_btn.setFixedWidth(240)
        #
        self.face_clear_lines_btn = QtWidgets.QPushButton('Clear Lines')
        self.face_clear_lines_btn.setFixedWidth(120)
        face_add_line_widget.layout().addWidget(self.face_bulk_mod_btn)
        face_add_line_widget.layout().addWidget(QtWidgets.QFrame())
        face_add_line_widget.layout().addWidget(self.face_add_line_btn)
        face_add_line_widget.layout().addWidget(QtWidgets.QFrame())
        face_add_line_widget.layout().addWidget(self.face_clear_lines_btn)
        self.face_mocap_widget.layout().addWidget(face_add_line_widget)
        # Bulk modifications -------------------------------------------------------------------------------------------
        face_bulk_mod_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 4, 'top', height=20)
        self.face_bulk_control_le = QtWidgets.QLineEdit()
        # self.face_bulk_control_le.setFixedWidth(120)
        face_bulk_mod_widget.layout().addWidget(self.face_bulk_control_le)
        Splitter_Vert(face_bulk_mod_widget, 16)
        #
        self.bulk_mod_cb = QtWidgets.QCheckBox()
        face_bulk_mod_widget.layout().addWidget(self.bulk_mod_cb)
        self.bulk_mod_combo = QtWidgets.QComboBox()
        self.bulk_mod_combo.addItem('T')
        self.bulk_mod_combo.addItem('R')
        self.bulk_mod_combo.setFixedWidth(40)
        face_bulk_mod_widget.layout().addWidget(self.bulk_mod_combo)
        Splitter_Vert(face_bulk_mod_widget, 16)
        #
        self.bulk_mult_X_cb = QtWidgets.QCheckBox()
        face_bulk_mod_widget.layout().addWidget(self.bulk_mult_X_cb)
        self.bulk_mult_X_le = QtWidgets.QLineEdit('1')
        self.bulk_mult_X_le.setFixedWidth(32)
        face_bulk_mod_widget.layout().addWidget(self.bulk_mult_X_le)
        #
        self.bulk_mult_Y_cb = QtWidgets.QCheckBox()
        face_bulk_mod_widget.layout().addWidget(self.bulk_mult_Y_cb)
        self.bulk_mult_Y_le = QtWidgets.QLineEdit('1')
        self.bulk_mult_Y_le.setFixedWidth(32)
        face_bulk_mod_widget.layout().addWidget(self.bulk_mult_Y_le)
        #
        self.bulk_mult_Z_cb = QtWidgets.QCheckBox()
        face_bulk_mod_widget.layout().addWidget(self.bulk_mult_Z_cb)
        self.bulk_mult_Z_le = QtWidgets.QLineEdit('1')
        self.bulk_mult_Z_le.setFixedWidth(32)
        face_bulk_mod_widget.layout().addWidget(self.bulk_mult_Z_le)
        Splitter_Vert(face_bulk_mod_widget, 16)
        #
        self.bulk_axes_cb = QtWidgets.QCheckBox()
        face_bulk_mod_widget.layout().addWidget(self.bulk_axes_cb)
        self.bulk_axes_combo = QtWidgets.QComboBox()
        self.bulk_axes_combo.setFixedWidth(48)
        self.bulk_axes_combo.addItem('xyz')
        self.bulk_axes_combo.addItem('xy')
        self.bulk_axes_combo.addItem('yz')
        self.bulk_axes_combo.addItem('xz')
        self.bulk_axes_combo.addItem('x')
        self.bulk_axes_combo.addItem('y')
        self.bulk_axes_combo.addItem('z')
        self.bulk_axes_combo.addItem('None')
        face_bulk_mod_widget.layout().addWidget(self.bulk_axes_combo)
        Splitter_Vert(face_bulk_mod_widget, 16)
        #
        self.bulk_mapping_cb = QtWidgets.QCheckBox()
        face_bulk_mod_widget.layout().addWidget(self.bulk_mapping_cb)
        self.bulk_mapping_combo = QtWidgets.QComboBox()
        self.bulk_mapping_combo.setFixedWidth(76)
        self.bulk_mapping_combo.addItem('xyz > xyz')
        self.bulk_mapping_combo.addItem('xyz > yzx')
        self.bulk_mapping_combo.addItem('xyz > zxy')
        self.bulk_mapping_combo.addItem('xyz > xzy')
        self.bulk_mapping_combo.addItem('xyz > yxz')
        self.bulk_mapping_combo.addItem('xyz > zyx')
        face_bulk_mod_widget.layout().addWidget(self.bulk_mapping_combo)
        #
        self.face_mocap_widget.layout().addWidget(face_bulk_mod_widget)
        #
        Splitter_Hor(self.face_mocap_widget, 6)
        # Load Anim Mesh -----------------------------------------------------------------------------------------------
        face_load_anim_mesh_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 6, 'left', height=20)
        self.face_mocap_widget.layout().addWidget(face_load_anim_mesh_widget)
        #
        self.face_load_anim_mesh_btn = QtWidgets.QPushButton('Load Anim Mesh')
        self.face_load_anim_mesh_btn.setFixedWidth(120)
        face_load_anim_mesh_widget.layout().addWidget(self.face_load_anim_mesh_btn)
        Splitter_Vert(face_load_anim_mesh_widget, 6)
        #
        self.face_anim_mesh_le = QtWidgets.QLineEdit('')
        face_load_anim_mesh_widget.layout().addWidget(self.face_anim_mesh_le)
        #
        Splitter_Hor(self.face_mocap_widget, 6)
        # Load Zero Mesh -----------------------------------------------------------------------------------------------
        face_load_zero_mesh_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 6, 'left', height=20)
        self.face_mocap_widget.layout().addWidget(face_load_zero_mesh_widget)
        #
        self.face_load_zero_mesh_btn = QtWidgets.QPushButton('Load Zero Mesh')
        self.face_load_zero_mesh_btn.setFixedWidth(120)
        face_load_zero_mesh_widget.layout().addWidget(self.face_load_zero_mesh_btn)
        Splitter_Vert(face_load_zero_mesh_widget, 6)
        #
        self.face_zero_mesh_le = QtWidgets.QLineEdit('')
        face_load_zero_mesh_widget.layout().addWidget(self.face_zero_mesh_le)
        #
        Splitter_Hor(self.face_mocap_widget, 6)
        # Posing controls ----------------------------------------------------------------------------------------------
        face_posing_controls_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 6, 'left', height=20)
        self.face_mocap_widget.layout().addWidget(face_posing_controls_widget)
        #
        self.face_apply_pose_btn = QtWidgets.QPushButton('Apply Pose')
        self.face_apply_pose_btn.setFixedWidth(120)
        face_posing_controls_widget.layout().addWidget(self.face_apply_pose_btn)

        #
        self.face_reset_pose_btn = QtWidgets.QPushButton('Reset Face')
        self.face_reset_pose_btn.setFixedWidth(110)
        face_posing_controls_widget.layout().addWidget(self.face_reset_pose_btn)
        #
        self.face_key_pose_btn = QtWidgets.QPushButton('Set Keyframe')
        self.face_key_pose_btn.setFixedWidth(110)
        face_posing_controls_widget.layout().addWidget(self.face_key_pose_btn)
        #
        self.face_remove_key_btn = QtWidgets.QPushButton('Remove Keyframe')
        self.face_remove_key_btn.setFixedWidth(110)
        face_posing_controls_widget.layout().addWidget(self.face_remove_key_btn)
        #
        self.face_select_controls_btn = QtWidgets.QPushButton('Select Controls')
        self.face_select_controls_btn.setFixedWidth(110)
        face_posing_controls_widget.layout().addWidget(self.face_select_controls_btn)

        #
        Splitter_Hor(self.face_mocap_widget, 6)
        # Bake animation -----------------------------------------------------------------------------------------------
        face_bake_anim_widget = Custom_Layout_Widget('hor', (0, 0, 0, 0), 6, 'left', height=20)
        self.face_mocap_widget.layout().addWidget(face_bake_anim_widget)
        #
        self.face_bake_anim_btn = QtWidgets.QPushButton('Bake Animation')
        self.face_bake_anim_btn.setFixedWidth(120)
        face_bake_anim_widget.layout().addWidget(self.face_bake_anim_btn)
        Splitter_Vert(face_bake_anim_widget, 6)
        #
        face_start_bake_lb = QtWidgets.QLabel('Start Frame:')
        face_start_bake_lb.setFixedWidth(60)
        face_bake_anim_widget.layout().addWidget(face_start_bake_lb)
        #
        self.face_start_bake_le = QtWidgets.QLineEdit('1')
        self.face_start_bake_le.setFixedWidth(40)
        face_bake_anim_widget.layout().addWidget(self.face_start_bake_le)
        #
        Splitter_Vert(face_bake_anim_widget, 8)
        #
        face_end_bake_lb = QtWidgets.QLabel('End Frame:')
        face_end_bake_lb.setFixedWidth(60)
        face_bake_anim_widget.layout().addWidget(face_end_bake_lb)
        #
        self.face_end_bake_le = QtWidgets.QLineEdit('120')
        self.face_end_bake_le.setFixedWidth(40)
        face_bake_anim_widget.layout().addWidget(self.face_end_bake_le)
        #
        Splitter_Vert(face_bake_anim_widget, 8)
        #
        face_bake_interval_lb = QtWidgets.QLabel('Interval:')
        face_bake_interval_lb.setFixedWidth(60)
        face_bake_anim_widget.layout().addWidget(face_bake_interval_lb)
        #
        self.face_bake_interval_le = QtWidgets.QLineEdit('1')
        self.face_bake_interval_le.setFixedWidth(40)
        face_bake_anim_widget.layout().addWidget(self.face_bake_interval_le)

    def init_signals(self):
        self.root_to_names_btn.clicked.connect(self.fill_in_mocap_joints_names)
        self.body_add_line_btn.clicked.connect(self.add_body_control_line)
        self.body_save_template_btn.clicked.connect(self.save_body_UI_template_file)
        self.body_load_template_btn.clicked.connect(self.load_body_UI_template_file)
        #
        self.body_create_init_pose_btn.clicked.connect(self.set_body_init_pose)
        self.body_save_init_pose_btn.clicked.connect(self.save_body_init_template_file)
        self.body_load_init_pose_btn.clicked.connect(self.load_body_init_template_file)
        #
        self.body_mirror_joint_btn.clicked.connect(self.mirror_transform_position)
        #
        self.body_bind_controls_btn.clicked.connect(self.bind_body_rig_to_mocap)
        #
        self.body_bake_anim_btn.clicked.connect(self.bake_body_animation)
        #
        self.load_selection_btn.clicked.connect(self.fill_in_face_controls_names)
        self.face_save_template_btn.clicked.connect(self.save_face_UI_template_file)
        self.face_load_template_btn.clicked.connect(self.load_face_UI_template_file)
        #
        self.find_target_objects_btn.clicked.connect(self.find_target_points)
        self.create_ref_objects_btn.clicked.connect(self.create_reference_objects)
        #
        self.face_add_line_btn.clicked.connect(self.add_face_control_line)
        self.face_clear_lines_btn.clicked.connect(lambda: self._clear_lines(self.face_joints_controls_lines_list))
        self.face_bulk_mod_btn.clicked.connect(self.face_bulk_modify_lines)
        #
        self.face_load_anim_mesh_btn.clicked.connect(lambda: self.load_object_name_to_field(self.face_anim_mesh_le))
        self.face_load_zero_mesh_btn.clicked.connect(lambda: self.load_object_name_to_field(self.face_zero_mesh_le))
        #
        self.face_apply_pose_btn.clicked.connect(self.transform_all_face_controllers)
        self.face_reset_pose_btn.clicked.connect(self.reset_face_pose)
        self.face_key_pose_btn.clicked.connect(self.keyframe_face)
        self.face_remove_key_btn.clicked.connect(self.remove_keyframe_face)
        self.face_select_controls_btn.clicked.connect(self.select_face_controls)
        self.face_bake_anim_btn.clicked.connect(self.bake_face_animation)

    # UI Functions
    # Body
    def add_body_control_line(self):
        self.body_joints_controls_lines_list.append(
            Joints_Pair_Body(self.body_joints_widget, self.body_joints_controls_lines_list))

    def save_body_UI_template_file(self):
        # Get Joint Pair line data
        def _get_joint_line_data(line_obj):
            mocap_joint = str(line_obj.mocap_joint_name)
            control_obj = str(line_obj.rig_control_name)
            r_axes = str(line_obj.R_options)
            t_axes = str(line_obj.T_options)
            id = str(line_obj.id)
            return [mocap_joint, control_obj, r_axes, t_axes, id]

        file_dialog = QtWidgets.QFileDialog()
        path = file_dialog.getSaveFileName(caption='Save Template File', filter='Text Documents (*.txt)')
        if (type(path) == str):
            self.body_template_le.setText(path)
        elif (type(path) == tuple):
            self.body_template_le.setText(path[0])

        # Record lines data
        outString = ''
        for item in self.body_joints_controls_lines_list:
            outString += '%s\n' % str(_get_joint_line_data(item))
        # Record UI data
        outString += '---//---\n'
        outString += '%s\n' % self.body_init_pose_frame_le.text()
        outString += '%s\n' % self.body_mirror_left_ID_le.text()
        outString += '%s\n' % self.body_mirror_right_ID_le.text()
        outString += '%s\n' % self.body_start_bake_le.text()
        outString += '%s\n' % self.body_end_bake_le.text()
        outString += '%s\n' % self.body_bake_interval_le.text()
        # Save to a file
        with open(path[0], 'w') as file:
            file.write(outString)

    def load_body_UI_template_file(self):
        file_dialog = QtWidgets.QFileDialog()
        path = file_dialog.getOpenFileName(caption='Load Template File', filter='Text Documents (*.txt)')
        if (path[0] == ''):
            return None
        elif (type(path) == str):
            self.body_template_le.setText(path)
        elif (type(path) == tuple):
            self.body_template_le.setText(path[0])
        # Read file
        inString = ''
        with open(path[0], 'r') as file:
            inString = file.read()
        # Divide inString
        lines_data = inString.split('\n---//---\n')[0]
        UI_data = inString.split('\n---//---\n')[1]
        # Splitting the lines
        lines_list = [ast.literal_eval(x) for x in lines_data.split('\n')]
        # Splitting UI data
        UI_data_list = UI_data.split('\n')

        # Delete all lines
        self._update_joint_lines_list(lines_list)
        # Fill in UI
        if (type(UI_data_list) == list and len(UI_data_list) >= 6):
            self.body_init_pose_frame_le.setText(UI_data_list[0])
            self.body_mirror_left_ID_le.setText(UI_data_list[1])
            self.body_mirror_right_ID_le.setText(UI_data_list[2])
            self.body_start_bake_le.setText(UI_data_list[3])
            self.body_end_bake_le.setText(UI_data_list[4])
            self.body_bake_interval_le.setText(UI_data_list[5])

    def fill_in_mocap_joints_names(self):
        joints_list = list_mocap_joints()
        self._update_joint_lines_list(joints_list)

    # Face
    def add_face_control_line(self):
        self.face_joints_controls_lines_list.append(
            Control_Pair_Face(self.face_controls_widget, self.face_joints_controls_lines_list))

    def fill_in_face_controls_names(self):
        controls_list = load_scene_selection()
        self._update_face_controls_lines_list(controls_list)

    def save_face_UI_template_file(self):
        # Get Joint Pair line data
        def _get_joint_line_data(line_obj):
            control_obj = str(line_obj.rig_control_name)
            source_obj = str(line_obj.source_object_name)
            mode = str(line_obj.mode)
            mult_X = str(line_obj.mult_X)
            mult_Y = str(line_obj.mult_Y)
            mult_Z = str(line_obj.mult_Z)
            axes_options = str(line_obj.axes_options)
            mapping_options = str(line_obj.mapping_options)
            return [control_obj, source_obj, mode, mult_X, mult_Y, mult_Z, axes_options, mapping_options]

        file_dialog = QtWidgets.QFileDialog()
        path = file_dialog.getSaveFileName(caption='Save Template File', filter='Text Documents (*.txt)')
        if (type(path) == str):
            self.face_template_le.setText(path)
        elif (type(path) == tuple):
            self.face_template_le.setText(path[0])

        # Record lines data
        outString = ''
        for item in self.face_joints_controls_lines_list:
            outString += '%s\n' % str(_get_joint_line_data(item))
        # Record UI data
        outString += '---//---\n'
        outString += '%s\n' % self.face_anim_mesh_le.text()
        outString += '%s\n' % self.face_zero_mesh_le.text()
        outString += '%s\n' % self.face_start_bake_le.text()
        outString += '%s\n' % self.face_end_bake_le.text()
        outString += '%s\n' % self.face_bake_interval_le.text()
        outString += '%s\n' % self.target_objects_prefix_le.text()
        # Save to a file
        with open(path[0], 'w') as file:
            file.write(outString)

    def load_face_UI_template_file(self):
        file_dialog = QtWidgets.QFileDialog()
        path = file_dialog.getOpenFileName(caption='Load Template File', filter='Text Documents (*.txt)')
        if (path[0] == ''):
            return None
        elif (type(path) == str):
            self.face_template_le.setText(path)
        elif (type(path) == tuple):
            self.face_template_le.setText(path[0])
        # Read file
        inString = ''
        with open(path[0], 'r') as file:
            inString = file.read()
        # Divide inString
        lines_data = inString.split('\n---//---\n')[0]
        UI_data = inString.split('\n---//---\n')[1]
        # Splitting the lines
        lines_list = [ast.literal_eval(x) for x in lines_data.split('\n')]
        # Splitting UI data
        UI_data_list = UI_data.split('\n')

        # Delete all lines
        self._update_face_controls_lines_list(lines_list)
        # Fill in UI
        if (type(UI_data_list) == list and len(UI_data_list) >= 6):
            self.face_anim_mesh_le.setText(UI_data_list[0])
            self.face_zero_mesh_le.setText(UI_data_list[1])
            self.face_start_bake_le.setText(UI_data_list[2])
            self.face_end_bake_le.setText(UI_data_list[3])
            self.face_bake_interval_le.setText(UI_data_list[4])
            self.target_objects_prefix_le.setText(UI_data_list[5])

    def load_object_name_to_field(self, field):
        mesh = load_scene_selection()[0]
        field.setText(mesh)

    def face_bulk_modify_lines(self):
        # Catch values
        mode = self.bulk_mod_combo.currentText()
        mult_X = self.bulk_mult_X_le.text()
        mult_Y = self.bulk_mult_Y_le.text()
        mult_Z = self.bulk_mult_Z_le.text()
        axes = self.bulk_axes_combo.currentText()
        mapping = self.bulk_mapping_combo.currentText()
        # Partial name
        controls_string = self.face_bulk_control_le.text()
        # Apply
        if (controls_string == ''):
            print('Partial name field is empty. Please, type in a common part for the lines you wish to modify.')
            return None
        for line in self.face_joints_controls_lines_list:
            sides = controls_string.split('not:')
            if (len(sides) < 2):
                sides.append('')
            include_list = sides[0].split(',')
            exclude_list = sides[1].split(',')
            include_list = [str(x.replace(' ', '')) for x in include_list]
            exclude_list = [str(x.replace(' ', '')) for x in exclude_list]
            if (exclude_list == ['']):
                del exclude_list[:]
            # print(include_list)
            # print(exclude_list)

            for name_part in include_list:
                # Exclusion
                if (name_part not in line.rig_control_name):
                    continue
                exclude_count = 0
                for exclude_part in exclude_list:
                    if (exclude_part in line.rig_control_name and exclude_count != ''):
                        exclude_count += 1
                if (exclude_count > 0):
                    # print(exclude_count)
                    continue
                # Mode
                if (mode == 'T' and self.bulk_mod_cb.isChecked()):
                    line.translate_mode_rb.setChecked(True)
                if (mode == 'R' and self.bulk_mod_cb.isChecked()):
                    line.rotate_mode_rb.setChecked(True)
                # Multipliers
                if (mult_X[-1].isdigit() and self.bulk_mult_X_cb.isChecked()):
                    line.mult_X_le.setText(mult_X)
                if (mult_Y[-1].isdigit() and self.bulk_mult_Y_cb.isChecked()):
                    line.mult_Y_le.setText(mult_Y)
                if (mult_Z[-1].isdigit() and self.bulk_mult_Z_cb.isChecked()):
                    line.mult_Z_le.setText(mult_Z)
                # Axes
                if (self.bulk_axes_cb.isChecked()):
                    line.axes_options_cb.setCurrentText(axes)
                # Mapping
                if (self.bulk_mapping_cb.isChecked()):
                    line.mapping_options_cb.setCurrentText(mapping)
                # Kick
                self.update_face_line_list_values(line)

    def update_face_line_list_values(self, line):
        line._axes_options_update()
        line._mapping_options_update()
        line._update_mode_value()
        line._update_mult_value()
        line._update_mult_value()
        line._update_mult_value()
        line._update_rig_control_name()
        line._update_source_object_name()

    # Shared functions
    def _clear_lines(self, lines_list):
        # Delete all lines
        for line in lines_list:
            line.deleteLater()
            del line
        del lines_list[:]

    def _update_joint_lines_list(self, lines_list):
        # Delete all lines
        for item in self.body_joints_controls_lines_list:
            item.deleteLater()
            del item
        del self.body_joints_controls_lines_list[:]
        # Recreate lines from the list
        if (type(lines_list) == list and len(lines_list) > 0):
            for line in lines_list:
                if (type(line) == str):
                    self.body_joints_controls_lines_list.append(
                        Joints_Pair_Body(self.body_joints_widget, self.body_joints_controls_lines_list, line))
                elif (type(line) == list):
                    self.body_joints_controls_lines_list.append(
                        Joints_Pair_Body(self.body_joints_widget, self.body_joints_controls_lines_list,
                                         line[0], line[1], line[2], line[3], line[4]))

    def _update_face_controls_lines_list(self, lines_list):
        # Recreate lines from the list
        if (type(lines_list) == list and len(lines_list) > 0):
            for line in lines_list:
                if (type(line) == str):
                    self.face_joints_controls_lines_list.append(
                        Control_Pair_Face(self.face_controls_widget, self.face_joints_controls_lines_list, line))
                elif (type(line) == list):
                    self.face_joints_controls_lines_list.append(
                        Control_Pair_Face(self.face_controls_widget, self.face_joints_controls_lines_list,
                                          control_name=line[0],
                                          source_object=line[1],
                                          mode=line[2],
                                          mult_X=line[3], mult_Y=line[4], mult_Z=line[5],
                                          axes_opt=line[6],
                                          mapping_opt=line[7]))

    def _list_face_controls(self):
        out_list = [x.rig_control_name for x in self.face_joints_controls_lines_list]
        return out_list

    def _list_face_controls_with_attributes(self):
        out_list = []
        for line in self.face_joints_controls_lines_list:
            control = line.rig_control_name
            mode = line.mode
            if (mode == 'T'):
                attrs = ('tx', 'ty', 'tz')
                for attr in attrs:
                    out_list.append('%s.%s' % (control, attr))
            if (mode == 'R'):
                attrs = ('rx', 'ry', 'rz')
                for attr in attrs:
                    out_list.append('%s.%s' % (control, attr))
        return out_list

    def _string_to_list(self, in_string):
        new_string = in_string.replace(' ', '')
        out_list = new_string.split(',')
        return out_list

    # Scene functions
    # Body
    def set_body_init_pose(self):
        init_frame = int(self.body_init_pose_frame_le.text())
        # Read mocap ROOT and rig COG names
        COG = self.body_joints_controls_lines_list[0].rig_control_name
        root = self.body_joints_controls_lines_list[0].mocap_joint_name
        # Read names of: Head_Joint, Head_Control, Foot_Joint, Foot_Control
        head_joint = ''
        head_control = ''
        foot_joint = ''
        foot_control = ''
        for line in self.body_joints_controls_lines_list:
            if (line.id == 'Head'):
                head_joint = line.mocap_joint_name
                head_control = line.rig_control_name
            elif (line.id == 'Foot'):
                foot_joint = line.mocap_joint_name
                foot_control = line.rig_control_name
            else:
                continue

        zero_pose_main(init_frame, root, COG, head_joint, head_control, foot_joint, foot_control)

    def save_body_init_template_file(self):
        root = self.body_joints_controls_lines_list[0].mocap_joint_name
        file_dialog = QtWidgets.QFileDialog()
        path = file_dialog.getSaveFileName(caption='Save Template File', filter='Text Documents (*.txt)')

        save_zero_pose_template(str(path[0]), root)

    def load_body_init_template_file(self):
        file_dialog = QtWidgets.QFileDialog()
        path = file_dialog.getOpenFileName(caption='Save Template File', filter='Text Documents (*.txt)')

        init_frame = int(self.body_init_pose_frame_le.text())

        load_zero_pose_from_template(str(path[0]), init_frame)

    def mirror_transform_position(self):
        left_ID = self.body_mirror_left_ID_le.text()
        right_ID = self.body_mirror_right_ID_le.text()

        if (left_ID != '' and right_ID != ''):
            mirror_counterpart_transforms(left_ID, right_ID)

    def bind_body_rig_to_mocap(self):
        mocap_to_rig_dict = {}
        mocap_to_R_axes_dict = {}
        mocap_to_T_axes_dict = {}
        for line in self.body_joints_controls_lines_list:
            mocap_to_rig_dict[line.mocap_joint_name] = line.rig_control_name
            mocap_to_R_axes_dict[line.mocap_joint_name] = line.R_options
            mocap_to_T_axes_dict[line.mocap_joint_name] = line.T_options

        bind_controls_to_mocap(mocap_to_rig_dict, mocap_to_R_axes_dict, mocap_to_T_axes_dict)

    # Face
    def create_reference_objects(self):
        prefix = self.target_objects_prefix_le.text()
        if (prefix == ''):
            return None
        controls_list = [x.rig_control_name for x in self.face_joints_controls_lines_list]

        create_reference_objects(controls_list, prefix)

    def reset_face_pose(self):
        attrs_list = self._list_face_controls_with_attributes()
        zero_attributes(attrs_list)

    def keyframe_face(self):
        attrs_list = self._list_face_controls_with_attributes()
        key_attributes(attrs_list)

    def remove_keyframe_face(self):
        attrs_list = self._list_face_controls_with_attributes()
        remove_key_from_attributes(attrs_list)

    def select_face_controls(self):
        controls_list = self._list_face_controls()
        select_objects(controls_list)

    def find_target_points(self):
        for line in self.face_joints_controls_lines_list:
            if (line.source_object_le.text() != ''):
                continue
            mesh = self.face_zero_mesh_le.text()
            control_obj = line.rig_control_name
            if (mesh == '' or control_obj == ''):
                continue
            max_points = int(self.max_target_number_le.text())
            prefix = self.target_objects_prefix_le.text()
            ref_object = '%s_%s' % (prefix, control_obj)
            target_points = find_closest_objects(max_points, mesh, ref_object)
            # Add reference points to UI
            line_str = str(target_points)[1:]
            line_str = line_str[:-1]
            line_str = line_str.replace('\'', '')
            line.source_object_le.setText(line_str)

    def transform_controller(self, line):
        if (line.source_object_name == ''):
            print('Skipped: %s' % line.rig_control_name)
            return None
        anim_mesh = self.face_anim_mesh_le.text()
        init_mesh = self.face_zero_mesh_le.text()
        point_list = self._string_to_list(line.source_object_name)
        controller = line.rig_control_name
        axes = line.axes_options
        mapping = line.mapping_options
        mode = line.mode
        mult = (float(line.mult_X), float(line.mult_Y), float(line.mult_Z))

        set_controller_transforms_main(init_mesh, anim_mesh, point_list, controller, axes, mapping, mult, mode)

    def transform_all_face_controllers(self):
        for line in self.face_joints_controls_lines_list:
            self.transform_controller(line)
        for line in self.face_joints_controls_lines_list:
            self.transform_controller(line)

    # Bake Animation
    def bake_body_animation(self):
        # Store control names
        controls = [x.rig_control_name for x in self.body_joints_controls_lines_list]
        # Read 'Start Frame'
        start_frame = int(self.body_start_bake_le.text())
        if (start_frame == '' or 'int' not in str(type(start_frame))):
            print('Check \'Start Frame\' field!')
            return None
        # Read 'End Frame'
        end_frame = int(self.body_end_bake_le.text())
        if (end_frame == '' or 'int' not in str(type(end_frame))):
            print('Check \'End Frame\' field!')
            return None
        # Read 'Step'
        step = int(self.body_bake_interval_le.text())
        if (step == '' or 'int' not in str(type(step))):
            print('Check \'Frame Interval\' field!')
            return None
        # Bake keys
        bake_body_animation(controls, start_frame, end_frame, step)
        # Finish message
        print('Done!')

    def bake_face_animation(self):
        start_frame = int(self.face_start_bake_le.text())
        end_frame = int(self.face_end_bake_le.text())
        interval = int(self.face_bake_interval_le.text())
        # Set frame
        curr_frame = start_frame
        while curr_frame <= end_frame:
            set_current_frame(curr_frame)
            self.transform_all_face_controllers()
            self.keyframe_face()
            curr_frame += interval


# UI Elements
class Custom_Layout_Widget(QtWidgets.QWidget):
    def __init__(self, direction='hor', margins=(0, 0, 0, 0), spacing=6, alignment='left', height=0, width=0):
        QtWidgets.QWidget.__init__(self)

        if (direction == 'hor'):
            self.setLayout(QtWidgets.QHBoxLayout())
        else:
            self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        self.layout().setSpacing(spacing)
        if (alignment == 'left'):
            self.layout().setAlignment(QtCore.Qt.AlignLeft)
        elif (alignment == 'right'):
            self.layout().setAlignment(QtCore.Qt.AlignRight)
        elif (alignment == 'top'):
            self.layout().setAlignment(QtCore.Qt.AlignTop)
        else:
            self.layout().setAlignment(QtCore.Qt.AlignBottom)

        if (height != 0):
            self.setFixedHeight(height)
        if (width != 0):
            self.setFixedWidth(width)


class Joints_Pair_Body(QtWidgets.QWidget):
    def __init__(self, parent, lines_list, jnt_name='', control_name='', R_opt='xyz', T_opt='xyz', id='None'):
        QtWidgets.QWidget.__init__(self)

        self.mocap_joint_name = jnt_name
        self.rig_control_name = control_name
        self.R_options = R_opt
        self.T_options = T_opt
        self.id = id

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(4)
        self.layout().setAlignment(QtCore.Qt.AlignLeft)
        # Joint field
        self.joint_le = QtWidgets.QLineEdit(jnt_name)
        # self.joint_le.setFixedWidth(140)
        self.layout().addWidget(self.joint_le)
        # Control field
        self.control_le = QtWidgets.QLineEdit(control_name)
        # self.control_le.setFixedWidth(140)
        self.layout().addWidget(self.control_le)
        Splitter_Vert(self, 2)
        # Pair button
        self.pair_btn = QtWidgets.QPushButton('pair')
        self.pair_btn.setFixedWidth(32)
        self.layout().addWidget(self.pair_btn)
        Splitter_Vert(self, 2)
        # Rotate options
        self.layout().addWidget(QtWidgets.QLabel('R:'))
        self.rotate_options_cb = QtWidgets.QComboBox()
        self.rotate_options_cb.setFixedWidth(48)
        self.rotate_options_cb.addItem('xyz')
        self.rotate_options_cb.addItem('xy')
        self.rotate_options_cb.addItem('yz')
        self.rotate_options_cb.addItem('xz')
        self.rotate_options_cb.addItem('x')
        self.rotate_options_cb.addItem('y')
        self.rotate_options_cb.addItem('z')
        self.rotate_options_cb.addItem('None')
        self.layout().addWidget(self.rotate_options_cb)
        # ---- Set combo to input value
        self.rotate_options_cb.setCurrentText(R_opt)
        # Translate options
        self.layout().addWidget(QtWidgets.QLabel('T:'))
        self.translate_options_cb = QtWidgets.QComboBox()
        self.translate_options_cb.setFixedWidth(48)
        self.translate_options_cb.addItem('xyz')
        self.translate_options_cb.addItem('xy')
        self.translate_options_cb.addItem('yz')
        self.translate_options_cb.addItem('xz')
        self.translate_options_cb.addItem('x')
        self.translate_options_cb.addItem('y')
        self.translate_options_cb.addItem('z')
        self.translate_options_cb.addItem('None')
        self.layout().addWidget(self.translate_options_cb)
        # ---- Set combo to input value
        self.translate_options_cb.setCurrentText(T_opt)
        Splitter_Vert(self, 2)
        # ID options
        self.id_options_cb = QtWidgets.QComboBox()
        self.id_options_cb.setFixedWidth(68)
        self.layout().addWidget(self.id_options_cb)
        self.id_options_cb.addItem('None')
        self.id_options_cb.addItem('Root')
        self.id_options_cb.addItem('Head')
        self.id_options_cb.addItem('Hand')
        self.id_options_cb.addItem('Foot')
        # ---- Set combo to input value
        self.id_options_cb.setCurrentText(id)
        self.layout().addWidget(QtWidgets.QFrame())
        # Delete button
        self.delete_btn = QtWidgets.QPushButton('X')
        self.delete_btn.setFixedSize(14, 14)
        self.layout().addWidget(self.delete_btn)
        self.layout().addWidget(QtWidgets.QFrame())

        # Signals
        self.pair_btn.clicked.connect(self._pair_button_action)
        #
        self.rotate_options_cb.currentIndexChanged.connect(self._rotate_options_update)
        self.rotate_options_cb.currentIndexChanged.connect(lambda: self._change_color(self.rotate_options_cb, 'black'))
        #
        self.translate_options_cb.currentIndexChanged.connect(self._translate_options_update)
        self.translate_options_cb.currentIndexChanged.connect(
            lambda: self._change_color(self.translate_options_cb, 'black'))
        #
        self.id_options_cb.currentIndexChanged.connect(self._id_options_update)
        self.id_options_cb.currentIndexChanged.connect(lambda: self._change_color(self.id_options_cb, 'black'))
        #
        self.joint_le.textChanged.connect(self._update_joint_name)
        self.control_le.textChanged.connect(self._update_control_name)
        self.delete_btn.clicked.connect(lambda: self._delete_item(lines_list))

        # Init
        self._init_values()
        # Parent
        parent.layout().addWidget(self)

    # Functions
    def _init_values(self):
        self.R_options = self.rotate_options_cb.currentText()
        self.T_options = self.translate_options_cb.currentText()
        self.id = self.id_options_cb.currentText()
        self.mocap_joint_name = self.joint_le.text()
        self.rig_control_name = self.control_le.text()

    def _pair_button_action(self):
        items = get_selection_items()
        if (len(items) == 2):
            self.joint_le.setText(items[0])
            self.control_le.setText(items[1])
        elif (len(items) == 1):
            self.control_le.setText(items[0])
        else:
            return None

    def _rotate_options_update(self):
        self.R_options = self.rotate_options_cb.currentText()
        print('\'%s\' rotate constraint set' % self.R_options)

    def _translate_options_update(self):
        self.T_options = self.translate_options_cb.currentText()
        print('\'%s\' translate constraint set' % self.T_options)

    def _id_options_update(self):
        self.id = self.id_options_cb.currentText()
        print('\'%s\' id set' % self.id)

    def _update_joint_name(self):
        self.mocap_joint_name = self.joint_le.text()
        # print('Mocap joint: %s' % self.mocap_joint_name)

    def _update_control_name(self):
        self.rig_control_name = self.control_le.text()
        # print('Rig control: %s' % self.rig_control_name)

    def _change_color(self, obj, color):
        obj.setStyleSheet('background-color: %s' % color)

    def _delete_item(self, lines_list):
        self.deleteLater()
        lines_list.remove(self)
        del self


class Control_Pair_Face(QtWidgets.QWidget):
    def __init__(self, parent, lines_list, control_name='', source_object='', mode='T', mult_X=1.0, mult_Y=1.0,
                 mult_Z=1.0, axes_opt='xyz', mapping_opt='xyz > xyz'):
        QtWidgets.QWidget.__init__(self)

        self.rig_control_name = control_name
        self.source_object_name = source_object
        self.axes_options = axes_opt
        self.mapping_options = mapping_opt
        self.mode = mode
        self.mult_X = mult_X
        self.mult_Y = mult_Y
        self.mult_Z = mult_Z

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(2)
        self.layout().setAlignment(QtCore.Qt.AlignLeft)
        # Joint field
        self.control_le = QtWidgets.QLineEdit(control_name)
        # self.control_le.setFixedWidth(136)
        self.layout().addWidget(self.control_le)
        # Control field
        self.source_object_le = QtWidgets.QLineEdit(source_object)
        # self.source_object_le.setFixedWidth(136)
        self.layout().addWidget(self.source_object_le)
        Splitter_Vert(self, 2)
        # Radio buttons
        mode_widget = Custom_Layout_Widget()
        self.layout().addWidget(mode_widget)
        #
        self.mode_rbg = QtWidgets.QButtonGroup(mode_widget)
        self.mode_rbg.setExclusive(True)
        #
        self.translate_mode_rb = QtWidgets.QRadioButton('T')
        if (mode == 'T'):
            self.translate_mode_rb.setChecked(True)
        mode_widget.layout().addWidget(self.translate_mode_rb)
        self.mode_rbg.addButton(self.translate_mode_rb)
        #
        self.rotate_mode_rb = QtWidgets.QRadioButton('R')
        if (mode == 'R'):
            self.rotate_mode_rb.setChecked(True)
        mode_widget.layout().addWidget(self.rotate_mode_rb)
        self.mode_rbg.addButton(self.rotate_mode_rb)
        Splitter_Vert(self, 2)
        # Mult
        self.mult_X_le = QtWidgets.QLineEdit(str(mult_X))
        self.mult_X_le.setFixedWidth(24)
        self.mult_Y_le = QtWidgets.QLineEdit(str(mult_Y))
        self.mult_Y_le.setFixedWidth(24)
        self.mult_Z_le = QtWidgets.QLineEdit(str(mult_Z))
        self.mult_Z_le.setFixedWidth(24)
        self.layout().addWidget(self.mult_X_le)
        self.layout().addWidget(self.mult_Y_le)
        self.layout().addWidget(self.mult_Z_le)
        Splitter_Vert(self, 2)
        # Axes options
        self.axes_options_cb = QtWidgets.QComboBox()
        self.axes_options_cb.setFixedWidth(48)
        self.axes_options_cb.addItem('xyz')
        self.axes_options_cb.addItem('xy')
        self.axes_options_cb.addItem('yz')
        self.axes_options_cb.addItem('xz')
        self.axes_options_cb.addItem('x')
        self.axes_options_cb.addItem('y')
        self.axes_options_cb.addItem('z')
        self.axes_options_cb.addItem('None')
        self.layout().addWidget(self.axes_options_cb)
        # ---- Set combo to input value
        self.axes_options_cb.setCurrentText(axes_opt)
        Splitter_Vert(self, 2)
        # Mapping options
        self.mapping_options_cb = QtWidgets.QComboBox()
        self.mapping_options_cb.setFixedWidth(76)
        self.mapping_options_cb.addItem('xyz > xyz')
        self.mapping_options_cb.addItem('xyz > yzx')
        self.mapping_options_cb.addItem('xyz > zxy')
        self.mapping_options_cb.addItem('xyz > xzy')
        self.mapping_options_cb.addItem('xyz > yxz')
        self.mapping_options_cb.addItem('xyz > zyx')
        self.layout().addWidget(self.mapping_options_cb)
        # ---- Set combo to input value
        self.mapping_options_cb.setCurrentText(mapping_opt)
        self.layout().addWidget(QtWidgets.QFrame())
        # Delete button
        self.delete_btn = QtWidgets.QPushButton('X')
        self.delete_btn.setFixedSize(14, 14)
        self.layout().addWidget(self.delete_btn)
        self.layout().addWidget(QtWidgets.QFrame())

        # Signals
        self.axes_options_cb.currentIndexChanged.connect(self._axes_options_update)
        self.axes_options_cb.currentIndexChanged.connect(lambda: self._change_color(self.axes_options_cb, 'black'))
        #
        self.mapping_options_cb.currentIndexChanged.connect(self._mapping_options_update)
        self.mapping_options_cb.currentIndexChanged.connect(
            lambda: self._change_color(self.mapping_options_cb, 'black'))
        #
        self.mode_rbg.buttonClicked.connect(self._update_mode_value)
        #
        self.mult_X_le.editingFinished.connect(self._update_mult_value)
        self.mult_Y_le.editingFinished.connect(self._update_mult_value)
        self.mult_Z_le.editingFinished.connect(self._update_mult_value)
        #
        self.control_le.textChanged.connect(self._update_rig_control_name)
        self.source_object_le.textChanged.connect(self._update_source_object_name)
        self.delete_btn.clicked.connect(lambda: self._delete_item(lines_list))

        # Init
        self._init_values()
        # Parent
        parent.layout().addWidget(self)

    # Functions
    def _init_values(self):
        self.axes_options = self.axes_options_cb.currentText()
        self.mapping_options = self.mapping_options_cb.currentText()
        if (self.translate_mode_rb.isChecked()):
            self.mode = 'T'
        else:
            self.mode = 'R'
        self.rig_control_name = self.control_le.text()
        self.source_object_name = self.source_object_le.text()

    def _update_mode_value(self):
        if (self.translate_mode_rb.isChecked() == True):
            self.mode = 'T'
        else:
            self.mode = 'R'

    def _update_mult_value(self):
        self.mult_X = float(self.mult_X_le.text())
        self.mult_Y = float(self.mult_Y_le.text())
        self.mult_Z = float(self.mult_Z_le.text())

    def _axes_options_update(self):
        self.axes_options = self.axes_options_cb.currentText()
        # print('\'%s\' rotate constraint set' % self.axes_options)

    def _mapping_options_update(self):
        self.mapping_options = self.mapping_options_cb.currentText()
        # print('\'%s\' translate constraint set' % self.mapping_options)

    def _update_rig_control_name(self):
        self.rig_control_name = self.control_le.text()
        # print('Mocap joint: %s' % self.mocap_joint_name)

    def _update_source_object_name(self):
        self.source_object_name = self.source_object_le.text()
        # print('Rig control: %s' % self.rig_control_name)

    def _change_color(self, obj, color):
        obj.setStyleSheet('background-color: %s' % color)

    def _delete_item(self, lines_list):
        self.deleteLater()
        lines_list.remove(self)
        del self


class Splitter_Vert(QtWidgets.QWidget):
    def __init__(self, parent_layout, width=25):
        QtWidgets.QWidget.__init__(self)

        splitter = QtWidgets.QFrame()
        splitter.setFrameStyle(QtWidgets.QFrame.VLine)
        splitter.setFixedWidth(width)

        parent_layout.layout().addWidget(splitter)


class Splitter_Hor(QtWidgets.QWidget):
    def __init__(self, parent_layout, height=25):
        QtWidgets.QWidget.__init__(self)

        splitter = QtWidgets.QFrame()
        splitter.setFrameStyle(QtWidgets.QFrame.HLine)
        splitter.setFixedHeight(height)

        parent_layout.layout().addWidget(splitter)


# ACTIVATE UI
dialog = None


def create():
    global dialog
    if dialog is None:
        dialog = MoCap_UI()
    else:
        delete()
    dialog.show()


def delete():
    global dialog
    if dialog is None:
        return
    dialog.deleteLater()
    dialog = None


#----------------------------------------------------------- UTILS -----------------------------------------------------
# SCENE LISTING --------------------------------------------------------------------------------------------------------
def get_selection_items():
    items = cmds.ls(sl=True, tr=True)
    if (len(items) == 0):
        return items
    elif (len(items) > 2):
        cmds.warning('Select mocap joint first, then a rig control.')
        return []
    else:
        return items

def load_scene_selection():
    sel = cmds.ls(sl=True, tr=True)
    # Ordering list by DAG
    dag_list = cmds.ls(dag=True, tr=True)
    # Out
    out_list = [str(x) for x in dag_list if x in sel]
    return out_list

def list_mocap_joints():
    sel = cmds.ls(sl=True, type='joint')
    if (len(sel) < 1):
        cmds.warning('Select a Root joint first!')
        return None
    elif (len(sel) > 1):
        cmds.warning('Select only a Root joint!')
        return None
    joint_list = cmds.listRelatives(ad=True, type='joint')
    joint_list.insert(0, sel[0])
    # Ordering list by DAG
    dag_list = cmds.ls(dag=True, type='joint')
    dag_list = [x for x in dag_list if x in joint_list]

    dag_list = [str(x) for x in dag_list]

    return dag_list

# ZERO POSE UTILS ------------------------------------------------------------------------------------------------------
def zero_pose_main(frame, root, COG, head_joint, head_control, foot_joint, foot_control):
    # Set Zero Pose frame
    cmds.currentTime(frame)
    # Set joints to zero-rotation
    zero_joints_rotation(root)
    # Key rotation
    cmds.select(root, r=True)
    cmds.select(hi=True)
    for item in cmds.ls(sl=True, type='joint'):
        attrs = ['rx', 'ry', 'rz']
        for attr in attrs:
            cmds.setKeyframe('%s.%s' % (item, attr), 'BaseAnimation')
    # Create adjustment anim layer
    adj_layer = 'adjustment_layer'
    if (cmds.objExists(adj_layer) == False):
        cmds.animLayer(adj_layer)
    # Add mocap joints to the adjustment anim layer
    cmds.animLayer(adj_layer, e=True, addSelectedObjects=True)
    # Create a default key on the adjustment anim layer
    for item in cmds.ls(sl=True, type='joint'):
        attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
        for attr in attrs:
            cmds.setKeyframe('%s.%s' % (item, attr), al='adjustment_layer')

# Zero rotation values in a joint hierarchy
def zero_joints_rotation(root):
    # Record joint hierarchy from the root joint
    joint_list = cmds.listRelatives(root, ad=True, type='joint')
    cmds.rotate(0.0, 0.0, 0.0, root)
    cmds.transformLimits(root, rm=True)
    for jnt in joint_list:
        cmds.transformLimits(jnt, rm=True)
        cmds.rotate(0.0, 0.0, 0.0, jnt)

# Distance between two points
def distance(pos_A, pos_B):
    distance = math.sqrt((pos_A[0] - pos_B[0]) * (pos_A[0] - pos_B[0]) +
                         (pos_A[1] - pos_B[1]) * (pos_A[1] - pos_B[1]) +
                         (pos_A[2] - pos_B[2]) * (pos_A[2] - pos_B[2]))
    return distance

# Adjust skeleton scale to the rig's measurements
def calculate_skeleton_scale(head_joint, head_control, left_foot_joint, left_foot_control):
    # Head Joint position
    head_joint_pos = cmds.xform(head_joint, q=True, t=True, a=True, ws=True)
    # Head Control position
    head_control_pos = cmds.xform(head_control, q=True, t=True, a=True, ws=True)
    # Foot Joint position
    left_foot_joint_pos = cmds.xform(left_foot_joint, q=True, t=True, a=True, ws=True)
    # Foot Control position
    left_foot_control_pos = cmds.xform(left_foot_control, q=True, t=True, a=True, ws=True)

    # Mocap assumed height
    mocap_height = distance(head_joint_pos, left_foot_joint_pos)
    # Rig's assumed height
    rig_height = distance(head_control_pos, left_foot_control_pos)

    # Scale difference
    scale_ratio = round(rig_height / mocap_height, 2)

    return scale_ratio

# Zero attributes
def zero_attributes(attrs_list):
    for attr in attrs_list:
        if (cmds.objExists(attr) == False):
            continue
        try:
            cmds.setAttr(attr, 0.0)
        except:
            continue

# I/O ------------------------------------------------------------------------------------------------------------------
# Save zero pose template
def save_zero_pose_template(filePath, root):
    # sel = cmds.ls(sl=True, type='joint')
    # if (len(sel) != 1):
    #     cmds.error('Select mocap ROOT joint first!')
    cmds.select(root, r=True)
    joints_list = list_mocap_joints()

    outString = ''
    for item in joints_list:
        if (cmds.objExists(item)):
            pos = cmds.xform(item, q=True, t=True, a=True, ws=True)
            rot = cmds.xform(item, q=True, ro=True, a=True, ws=True)
            scl = cmds.xform(item, q=True, s=True, a=True, ws=True)
            outString += '%s : [%s, %s, %s, %s, %s, %s, %s, %s, %s]\n' % (item, pos[0], pos[1], pos[2],
                                                                                rot[0], rot[1], rot[2],
                                                                                scl[0], scl[1], scl[2])
    with open(filePath, 'w') as file:
        file.write(outString)
    print('Template: %s is saved!' % filePath)

# Load zero pose
def load_zero_pose_from_template(filePath, init_frame):
    with open(filePath, 'r') as file:
        inString = file.read()

    lines = inString.split('\n')
    lines = [x for x in lines if x!='']
    # Create adjustment anim layer
    adj_layer = 'adjustment_layer'
    if (cmds.objExists(adj_layer) == False):
        cmds.animLayer(adj_layer)
    # Set Zero Pose frame
    curr_min = cmds.playbackOptions(q=True, min=True)
    if (init_frame < curr_min):
        cmds.playbackOptions(min=init_frame)
    cmds.currentTime(init_frame)
    for line in lines:
        obj = line.split(' : ')[0]
        trs = ast.literal_eval(line.split(' : ')[1])
        if (cmds.objExists(obj)):
            # Create rotation key at zero
            attrs = ['rx', 'ry', 'rz']
            for attr in attrs:
                cmds.rotate(0, 0, 0, obj, a=True)
                cmds.setKeyframe('%s.%s' % (obj, attr), 'BaseAnimation')
            # Add mocap joints to the adjustment anim layer
            cmds.select(obj, r=True)
            cmds.animLayer(adj_layer, e=True, addSelectedObjects=True)
            # Position joint
            cmds.xform(obj, t =(trs[0], trs[1], trs[2]), a=True, ws=True)
            cmds.xform(obj, ro=(trs[3], trs[4], trs[5]), a=True, ws=True)
            cmds.xform(obj, s =(trs[6], trs[7], trs[8]), a=True, ws=True)
            # Create a default key on the adjustment anim layer
            attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
            for attr in attrs:
                cmds.setKeyframe('%s.%s' % (obj, attr), al='adjustment_layer')
    print('Loaded from %s' % filePath)

# MIRROR ---------------------------------------------------------------------------------------------------------------
def mirror_counterpart_transforms(left_id='Left', right_id='Right'):
    sel = cmds.ls(sl=True, tr=True)
    for obj in sel:
        if (left_id in obj):
            counterPart_obj = obj.replace(left_id, right_id)
        elif (right_id in obj):
            counterPart_obj = obj.replace(right_id, left_id)
        else:
            cmds.warning('No side marking in the object name. Skip...')
            continue
        if (cmds.objExists(counterPart_obj) == False):
            continue
        # Get attrs
        tx = cmds.getAttr('%s.tx' % obj) * (-1)
        ty = cmds.getAttr('%s.ty' % obj)
        tz = cmds.getAttr('%s.tz' % obj)

        rx = cmds.getAttr('%s.rx' % obj)
        ry = cmds.getAttr('%s.ry' % obj) * (-1)
        rz = cmds.getAttr('%s.rz' % obj) # * (-1)

        sx = cmds.getAttr('%s.sx' % obj)
        sy = cmds.getAttr('%s.sy' % obj)
        sz = cmds.getAttr('%s.sz' % obj)
        # Set Attrs
        cmds.setAttr('%s.tx' % counterPart_obj, tx)
        cmds.setAttr('%s.ty' % counterPart_obj, ty)
        cmds.setAttr('%s.tz' % counterPart_obj, tz)

        cmds.setAttr('%s.rx' % counterPart_obj, rx)
        cmds.setAttr('%s.ry' % counterPart_obj, ry)
        cmds.setAttr('%s.rz' % counterPart_obj, rz)

        cmds.setAttr('%s.sx' % counterPart_obj, sx)
        cmds.setAttr('%s.sy' % counterPart_obj, sy)
        cmds.setAttr('%s.sz' % counterPart_obj, sz)

# BIND -----------------------------------------------------------------------------------------------------------------
def bind_controls_to_mocap(mocap_to_rig_dict, mocap_to_R_axes_dict, mocap_to_T_axes_dict):
    # Filter out non-animated joints
    joints = []
    for key in mocap_to_rig_dict:
        if (mocap_to_rig_dict[key] != ''):
            joints.append(key)
    # Create top groups over controllers
    controllers = []
    for jnt in joints:
        controllers.append(mocap_to_rig_dict[jnt])
    # Parent constraint controllers to joints
    for jnt in joints:
        # print(jnt, mocap_to_rig_dict[jnt])
        constraint_name = 'constr_%s' % jnt
        # Skip Rotate
        skip_rotate = []
        if ('x' not in mocap_to_R_axes_dict[jnt] or cmds.getAttr('%s.rx' % mocap_to_rig_dict[jnt], k=True) == False):
            skip_rotate.append("x")
        if ('y' not in mocap_to_R_axes_dict[jnt] or cmds.getAttr('%s.ry' % mocap_to_rig_dict[jnt], k=True) == False):
            skip_rotate.append("y")
        if ('z' not in mocap_to_R_axes_dict[jnt] or cmds.getAttr('%s.rz' % mocap_to_rig_dict[jnt], k=True) == False):
            skip_rotate.append("z")
        # Skip Translate
        skip_translate = []
        if ('x' not in mocap_to_R_axes_dict[jnt] or cmds.getAttr('%s.tx' % mocap_to_rig_dict[jnt], k=True) == False):
            skip_translate.append("x")
        if ('y' not in mocap_to_R_axes_dict[jnt] or cmds.getAttr('%s.ty' % mocap_to_rig_dict[jnt], k=True) == False):
            skip_translate.append("y")
        if ('z' not in mocap_to_R_axes_dict[jnt] or cmds.getAttr('%s.tz' % mocap_to_rig_dict[jnt], k=True) == False):
            skip_translate.append("z")
        # Compose command
        cmd = 'cmds.parentConstraint("%s", "%s", mo=True, n="%s", sr=%s, st=%s)' % (jnt, mocap_to_rig_dict[jnt],
                                                                                    constraint_name,
                                                                              str(skip_rotate), str(skip_translate))

        exec(cmd)

# KEYING ---------------------------------------------------------------------------------------------------------------
def set_current_frame(frame):
    cmds.currentTime(frame)

def key_attributes(attrs_list):
    for attr in attrs_list:
        if (cmds.objExists(attr) == False):
            continue
        cmds.setKeyframe(attr)

def remove_key_from_attributes(attr_list):
    curr_frame = cmds.currentTime(q=True)
    for attr in attr_list:
        if (cmds.objExists(attr) == False):
            continue
        obj_attr = attr.split('.')
        cmds.cutKey(obj_attr[0], time=(curr_frame, curr_frame), at=obj_attr[1])

def select_objects(obj_list):
    filtered_list = [x for x in obj_list if cmds.objExists(x)]
    cmds.select(filtered_list, r=True)

# BAKE -----------------------------------------------------------------------------------------------------------------
# Bake animation on a list of controls
def bake_body_animation(controllers, start_frame, end_frame, step):
    attrs = ('tx', 'ty', 'tz', 'rx', 'ry', 'rz')
    for controller in controllers:
        if (cmds.objExists(controller) == False):
            continue
        for attr in attrs:
            cmds.bakeResults('%s.%s' % (controller, attr), t=(start_frame, end_frame), sb=step)

# FACE TARGET OBJECTS --------------------------------------------------------------------------------------------------
def create_reference_objects(controls_list, ref_prefix):
    for control in controls_list:
        if (cmds.objExists(control) == False):
            continue
        ref_obj = '%s_%s' % (ref_prefix, control)
        cmds.spaceLocator(n=ref_obj)
        cmds.scale(.1, .1, .1, ref_obj)
        pos = cmds.xform(control, q=True, t=True, ws=True, a=True)
        cmds.xform(ref_obj, t=pos, ws=True, a=True)

def find_closest_objects(max_num, mesh, ref_obj):
    if (cmds.objExists(ref_obj) == False):
        return ''
    ref_pos = cmds.xform(ref_obj, q=True, t=True, ws=True, a=True)
    if (mesh != '' and cmds.objExists(mesh)):
        num_points = cmds.polyEvaluate(mesh, v=True)
        closest_points = []
        dist_list = []
        dist_to_point_dict = {}
        for i in range(num_points):
            curr_point = '%s.vtx[%s]' % (mesh, i)
            point_pos = cmds.pointPosition(curr_point)
            curr_dist = round(distance(ref_pos, point_pos), 3)
            # Check if reference object is snapped to the point
            if (curr_dist < 0.0001):
                return [str(curr_point)]
            elif (curr_dist > 2.0):
                continue
            else:
                dist_list.append(curr_dist)
                dist_to_point_dict[curr_dist] = curr_point
        # Find closet points
        dist_list.sort()
        for i in range(max_num):
            closest_points.append(str(dist_to_point_dict[dist_list[i]]))

        return closest_points

def find_average_position(pos_list):
    pos_sum = [0.0, 0.0, 0.0]
    for pos in pos_list:
        pos_sum[0] += pos[0]
        pos_sum[1] += pos[1]
        pos_sum[2] += pos[2]

    num = len(pos_list)
    average_pos = (pos_sum[0]/num, pos_sum[1]/num, pos_sum[2]/num)
    return average_pos

def find_position_difference(pos_A, pos_B):
    return (pos_A[0] - pos_B[0], pos_A[1] - pos_B[1], pos_A[2] - pos_B[2])

def find_jaw_compensation(controller):
    ref_obj = controller.replace('poseJnt_', 'ref_zero_')
    if (cmds.objExists(ref_obj) == False or ref_obj == controller):
        return (0.0, 0.0, 0.0)
    ref_pos = cmds.xform(ref_obj, q=True, t=True, os=True)
    return ref_pos

def set_controller_transforms(obj, pos, axes, mapping, mult, mode):
    mult_dict = {'x':mult[0], 'y':mult[1], 'z':mult[2]}

    compensation = find_jaw_compensation(obj)
    maps = str(mapping).split(' > ')
    # Mapping dict
    map_dict = {maps[1][0] : maps[0][0], maps[1][1] : maps[0][1], maps[1][2] : maps[0][2]}
    # Posistion dict
    pos_dict = {}
    for i in range(3):
        pos_dict[maps[0][i]] = round(pos[i], 3)
    obj_pos = []
    for i in maps[0]:
        if (i not in axes):
            obj_pos.append(0)
        else:
            obj_pos.append(round(pos_dict[map_dict[i]] * mult_dict[i], 3))

    for i in range(3):
        obj_pos[i] -= compensation[i]
    obj_pos = tuple(obj_pos)

    if (mode == 'T'):
        cmds.xform(obj, t=obj_pos, a=True, os=True)
    elif (mode == 'R'):
        cmds.xform(obj, ro=obj_pos, a=True, os=True)
    else:
        return None

def set_controller_transforms_main(init_mesh, anim_mesh, point_list, controller, axes, mapping, mult, mode):
    init_pos_list = []
    anim_pos_list = []
    for point in point_list:
        if ('vtx' in point):
            init_point = '%s.%s' % (init_mesh, point.split('.')[1])
            anim_point = '%s.%s' % (anim_mesh, point.split('.')[1])
            init_pos_list.append(cmds.pointPosition(init_point))
            anim_pos_list.append(cmds.pointPosition(anim_point))
        elif (cmds.objExists(point) == True and cmds.objectType(point) == 'transform'):
            init_pos_list.append((0.0, 0.0, 0.0))
            anim_pos_list.append(cmds.xform(point, q=True, t=True, os=True, a=True))
    # Average point
    init_average_pos = find_average_position(init_pos_list)
    anim_average_pos = find_average_position(anim_pos_list)
    # Position difference
    pos_diff = find_position_difference(anim_average_pos, init_average_pos)
    # Move/Rotate controller
    set_controller_transforms(controller, pos_diff, axes, mapping, mult, mode)





