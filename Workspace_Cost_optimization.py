Description: "(SO0018) - cost-optimizer-for-amazon-workspaces: A solution for automatically optimizing the cost of Amazon Workspaces version v2.6.5"
Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: Select New or Existing VPC for AWS Fargate
        Parameters:
          - CreateNewVPC
      - Label:
          default: Existing VPC Settings
        Parameters:
          - ExistingSubnet1Id
          - ExistingSubnet2Id
          - ExistingSecurityGroupId
      - Label:
          default: New VPC Settings
        Parameters:
          - VpcCIDR
          - Subnet1CIDR
          - Subnet2CIDR
          - EgressCIDR
      - Label:
          default: Testing Parameters
        Parameters:
          - DryRun
          - TestEndOfMonth
          - LogLevel
      - Label:
          default: Inactivity Settings
        Parameters:
          - InactivityPowerOffDays
          - InactivityTerminateWarningDays
          - TerminationGracePeriodDays
      - Label:
          default: Pricing Parameters
        Parameters:
          - ValueLimit
          - StandardLimit
          - PerformanceLimit
          - GraphicsLimit
          - GraphicsProLimit
          - PowerLimit
          - PowerProLimit
      - Label:
          default: List of AWS Regions
        Parameters:
          - Regions
      - Label:
          default: Terminate unused workspaces
        Parameters:
          - TerminateUnusedWorkspaces
          - NumberOfMonthsForTerminationCheck
      - Label:
          default: Multi account deployment
        Parameters:
          - OrganizationID
          - ManagementAccountId
    ParameterLabels:
      VpcCIDR:
        default: AWS Fargate VPC CIDR Block
      Subnet1CIDR:
        default: AWS Fargate Subnet 1 CIDR Block
      Subnet2CIDR:
        default: AWS Fargate Subnet 2 CIDR Block
      EgressCIDR:
        default: AWS Fargate SecurityGroup CIDR Block
      DryRun:
        default: Launch in Dry Run Mode
      TestEndOfMonth:
        default: Simulate End of Month Cleanup
      LogLevel:
        default: Log Level
      CreateNewVPC:
        default: Create New VPC
      ExistingSubnet1Id:
        default: Subnet ID for first subnet
      ExistingSubnet2Id:
        default: Subnet ID for second subnet
      ExistingSecurityGroupId:
        default: Security group ID to launch ECS task
      InactivityPowerOffDays:
        default: Days of inactivity before power off
      InactivityTerminateWarningDays:
        default: Days of inactivity before termination warning
      TerminationGracePeriodDays:
        default: Grace period days after warning before termination
      Regions:
        default: List of AWS Regions
      TerminateUnusedWorkspaces:
        default: Terminate workspaces not used for a month
      OrganizationID:
        default: Organization ID for multi account deployment
      ManagementAccountId:
        default: Account ID of the Management Account for the Organization
      NumberOfMonthsForTerminationCheck:
        default: Number of months for termination check
Parameters:
  CreateNewVPC:
    Type: String
    Default: "Yes"
    AllowedValues:
      - "Yes"
      - "No"
    Description: Select "Yes" to deploy the solution in a new VPC.
  ExistingSubnet1Id:
    Type: String
    Default: ""
    Description: Subnet ID to launch ECS task. Leave this blank is you selected "Yes" for "Create New VPC"
  ExistingSubnet2Id:
    Type: String
    Default: ""
    Description: Subnet ID to launch ECS task. Leave this blank is you selected "Yes" for "Create New VPC"
  ExistingSecurityGroupId:
    Type: String
    Default: ""
    Description: Security Group Id to launch ECS task. Leave this blank is you selected "Yes" for "Create New VPC"
  VpcCIDR:
    Type: String
    Default: 10.215.0.0/16
    AllowedPattern: (?:^$|(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2}))
    ConstraintDescription: must be a valid IP CIDR range of the form x.x.x.x/x.
    Description: This VPC launches containers. Change addresses only if it conflicts with your network.
    MaxLength: 18
    MinLength: 9
  Subnet1CIDR:
    Type: String
    Default: 10.215.10.0/24
    AllowedPattern: (?:^$|(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2}))
    ConstraintDescription: must be a valid IP CIDR range of the form x.x.x.x/x.
    MaxLength: 18
    MinLength: 9
  Subnet2CIDR:
    Type: String
    Default: 10.215.20.0/24
    AllowedPattern: (?:^$|(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2}))
    ConstraintDescription: must be a valid IP CIDR range of the form x.x.x.x/x.
    MaxLength: 18
    MinLength: 9
  EgressCIDR:
    Type: String
    Default: 0.0.0.0/0
    AllowedPattern: (?:^$|(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2}))
    ConstraintDescription: must be a valid IP CIDR range of the form x.x.x.x/x.
    Description: The Cidir Block to restrict the ECS container outbound access
    MaxLength: 18
    MinLength: 9
  LogLevel:
    Type: String
    Default: INFO
    AllowedValues:
      - CRITICAL
      - ERROR
      - INFO
      - WARNING
      - DEBUG
  DryRun:
    Type: String
    Default: "Yes"
    AllowedValues:
      - "Yes"
      - "No"
    Description: Solution will generate a change log, but not execute any changes.
  TestEndOfMonth:
    Type: String
    Default: "No"
    AllowedValues:
      - "Yes"
      - "No"
    Description: Overrides date and forces the solution to run as if it is the end of the month.
  Regions:
    Type: String
    Default: ""
    Description: The list of AWS regions which the solution will scan. Example - us-east-1, us-west-2. Leave blank to scan all regions.
  TerminateUnusedWorkspaces:
    Type: String
    Default: "No"
    AllowedValues:
      - "Yes"
      - "No"
      - Dry Run
    Description: Select "Yes" to terminate Workspaces not used for a month.
  ValueLimit:
    Type: Number
    Default: 81
    Description: The number of hours a Value instance can run in a month before being converted to ALWAYS_ON. Default is 81.
  StandardLimit:
    Type: Number
    Default: 85
    Description: The number of hours a Standard instance can run in a month before being converted to ALWAYS_ON. Default is 81.
  PerformanceLimit:
    Type: Number
    Default: 83
    Description: The number of hours a Performance instance can run in a month before being converted to ALWAYS_ON. Default is 81.
  PowerLimit:
    Type: Number
    Default: 83
    Description: The number of hours a Power instance can run in a month before being converted to ALWAYS_ON. Default is 81.
  PowerProLimit:
    Type: Number
    Default: 80
    Description: The number of hours a Power Pro instance can run in a month before being converted to ALWAYS_ON. Default is 81.
  GraphicsLimit:
    Type: Number
    Default: 217
    Description: The number of hours a Graphics instance can run in a month before being converted to ALWAYS_ON. Default is 81.
  GraphicsProLimit:
    Type: Number
    Default: 80
    Description: The number of hours a Graphics Pro instance can run in a month before being converted to ALWAYS_ON. Default is 81.
  OrganizationID:
    Type: String
    Default: ""
    AllowedPattern: ^$|^o-[a-z0-9]{10,32}$
    Description: Organization ID to support multi account deployment. Leave blank for single account deployments.
  ManagementAccountId:
    Type: String
    Default: ""
    Description: Account ID for the management account of the Organization. Leave blank for single account deployments.
  NumberOfMonthsForTerminationCheck:
    Type: String
    Default: "1"
    AllowedValues:
      - "1"
      - "2"
      - "3"
      - "4"
      - "5"
      - "6"
      - "7"
      - "8"
      - "9"
      - "10"
      - "11"
      - "12"
      - "13"
      - "14"
      - "15"
    Description: Provide the number of months to check for inactive period before termination. Default value is 1 month.
  InactivityPowerOffDays:
    Type: Number
    Default: 14
    Description: The number of days of inactivity before WorkSpaces are powered off.
  InactivityTerminateWarningDays:
    Type: Number
    Default: 30
    Description: The number of days of inactivity before users receive a termination warning.
  TerminationGracePeriodDays:
    Type: Number
    Default: 10
    Description: The grace period in days after the warning before WorkSpaces are terminated.
Mappings:
  Solution:
    Data:
      ClusterName: cost-optimizer-cluster
      TaskDefinitionName: wco-task
      LogGroupName: /ecs/wco-task
      ID: SO0018
      Version: v2.6.5
      SendAnonymousUsageData: "True"
      MetricsURL: https://metrics.awssolutionsbuilder.com/generic
      AutoStopTimeoutHours: 1
      Image: public.ecr.aws/aws-solutions/workspaces-cost-optimizer:v2.6.5
      RoleName: Workspaces-Cost-Optimizer
      RegisterLambdaFunctionName: Register-Spoke-Accounts
      SpokeAccountWorkspacesRole: Workspaces-Admin-Spoke
      TagKey: CloudFoundations:CostOptimizerForWorkspaces
      AppRegistryApplicationName: workspaces-cost-optimizer
      SolutionName: Cost Optimizer for Amazon Workspaces
Conditions:
  CreateNewVPCCondition:
    Fn::Equals:
      - Ref: CreateNewVPC
      - "Yes"
  UseExistingVPCCondition:
    Fn::Equals:
      - Ref: CreateNewVPC
      - "No"
  organizationIdInputParameter:
    Fn::Equals:
      - Ref: OrganizationID
      - ""
  managementIdInputParameter:
    Fn::Equals:
      - Ref: ManagementAccountId
      - ""
  ManagementAccountSetupCondition:
    Fn::Not:
      - Condition: managementIdInputParameter
  OrganizationSetupCondition:
    Fn::Not:
      - Condition: organizationIdInputParameter
  MultiAccountDeploymentCondition:
    Fn::And:
      - Condition: OrganizationSetupCondition
      - Condition: ManagementAccountSetupCondition
  CreateDynamoDBEndpointCondition:
    Fn::And:
      - Condition: CreateNewVPCCondition
      - Condition: MultiAccountDeploymentCondition
Resources:
  LogsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
    UpdateReplacePolicy: Retain
    DeletionPolicy: Retain
    Metadata:
      cfn_nag:
        rules_to_suppress:
          - id: W35
            reason: " Access logging is not required for this bucket."
          - id: W51
            reason: Policy is not required for this bucket.
  UsageReportBucketResourcesAccessLoggingBucketPolicyE13961AA:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket:
        Ref: LogsBucket
      PolicyDocument:
        Statement:
          - Action: s3:*
            Condition:
              Bool:
                aws:SecureTransport: "false"
            Effect: Deny
            Principal:
              AWS: "*"
            Resource:
              - Fn::GetAtt:
                  - LogsBucket
                  - Arn
              - Fn::Join:
                  - ""
                  - - Fn::GetAtt:
                        - LogsBucket
                        - Arn
                    - /*
          - Action: s3:PutObject
            Condition:
              ArnLike:
                aws:SourceArn:
                  Fn::GetAtt:
                    - CostOptimizerBucket
                    - Arn
              StringEquals:
                aws:SourceAccount:
                  Ref: AWS::AccountId
            Effect: Allow
            Principal:
              Service: logging.s3.amazonaws.com
            Resource:
              Fn::Join:
                - ""
                - - Fn::GetAtt:
                      - LogsBucket
                      - Arn
                  - /wco_bucket/*
        Version: "2012-10-17"
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/UsageReportBucketResources/AccessLoggingBucket/Policy/Resource
  CostOptimizerBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      LifecycleConfiguration:
        Rules:
          - ExpirationInDays: 365
            Id: DeletionRule
            Status: Enabled
      LoggingConfiguration:
        DestinationBucketName:
          Ref: LogsBucket
        LogFilePrefix: wco_bucket/
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
    UpdateReplacePolicy: Retain
    DeletionPolicy: Retain
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/UsageReportBucketResources/CostOptimizerBucket/Resource
  S3BucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket:
        Ref: CostOptimizerBucket
      PolicyDocument:
        Statement:
          - Action: s3:*
            Condition:
              Bool:
                aws:SecureTransport: "false"
            Effect: Deny
            Principal:
              AWS: "*"
            Resource:
              - Fn::GetAtt:
                  - CostOptimizerBucket
                  - Arn
              - Fn::Join:
                  - ""
                  - - Fn::GetAtt:
                        - CostOptimizerBucket
                        - Arn
                    - /*
        Version: "2012-10-17"
    Metadata:
      cfn_nag:
        rules_to_suppress:
          - id: W51
            reason: Policy is not required for this bucket.
  SpokeAccountTable:
    Type: AWS::DynamoDB::Table
    Properties:
      AttributeDefinitions:
        - AttributeName: account_id
          AttributeType: S
        - AttributeName: role_name
          AttributeType: S
      BillingMode: PAY_PER_REQUEST
      KeySchema:
        - AttributeName: account_id
          KeyType: HASH
        - AttributeName: role_name
          KeyType: RANGE
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      SSESpecification:
        SSEEnabled: true
    UpdateReplacePolicy: Retain
    DeletionPolicy: Retain
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/SpokeAccountTable/Resource
    Condition: MultiAccountDeploymentCondition
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock:
        Ref: VpcCIDR
      EnableDnsHostnames: true
      EnableDnsSupport: true
      InstanceTenancy: default
      Tags:
        - Key:
            Fn::FindInMap:
              - Solution
              - Data
              - TagKey
          Value:
            Ref: AWS::StackName
        - Key: Name
          Value: cost-optimizer-vpc
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/VPC
    Condition: CreateNewVPCCondition
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key:
            Fn::FindInMap:
              - Solution
              - Data
              - TagKey
          Value:
            Ref: AWS::StackName
        - Key: Name
          Value: cost-optimizer-igw
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/InternetGateway
    Condition: CreateNewVPCCondition
  Subnet1:
    Type: AWS::EC2::Subnet
    Properties:
      AvailabilityZone:
        Fn::Select:
          - 0
          - Fn::GetAZs: ""
      CidrBlock:
        Ref: Subnet1CIDR
      Tags:
        - Key: Name
          Value: cost-optimizer-vpc-subnet1
      VpcId:
        Ref: VPC
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/Subnet1
    Condition: CreateNewVPCCondition
  Subnet2:
    Type: AWS::EC2::Subnet
    Properties:
      AvailabilityZone:
        Fn::Select:
          - 1
          - Fn::GetAZs: ""
      CidrBlock:
        Ref: Subnet2CIDR
      Tags:
        - Key: Name
          Value: cost-optimizer-vpc-subnet2
      VpcId:
        Ref: VPC
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/Subnet2
    Condition: CreateNewVPCCondition
  IntraVPCSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group that allows inbound from the VPC and outbound to the Internet
      VpcId:
        Ref: VPC
    Metadata:
      cfn_nag:
        rules_to_suppress:
          - id: W36
            reason: flagged as not having a Description, property is GroupDescription not Description
          - id: W40
            reason: IpProtocol set to -1 (any) as ports are not known prior to running tests
    Condition: CreateNewVPCCondition
  MainRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId:
        Ref: VPC
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/MainRouteTable
    Condition: CreateNewVPCCondition
  InternetGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      InternetGatewayId:
        Ref: InternetGateway
      VpcId:
        Ref: VPC
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/InternetGatewayAttachment
    Condition: CreateNewVPCCondition
  SecurityGroupEgress:
    Type: AWS::EC2::SecurityGroupEgress
    Properties:
      CidrIp:
        Ref: EgressCIDR
      GroupId:
        Fn::GetAtt:
          - IntraVPCSecurityGroup
          - GroupId
      IpProtocol: "-1"
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/SecurityGroupEgress
    Condition: CreateNewVPCCondition
  RouteToInternet:
    Type: AWS::EC2::Route
    Properties:
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId:
        Ref: InternetGateway
      RouteTableId:
        Ref: MainRouteTable
    DependsOn:
      - InternetGatewayAttachment
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/RouteToInternet
    Condition: CreateNewVPCCondition
  Subnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId:
        Ref: MainRouteTable
      SubnetId:
        Fn::GetAtt:
          - Subnet1
          - SubnetId
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/Subnet1RouteTableAssociation
    Condition: CreateNewVPCCondition
  Subnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId:
        Ref: MainRouteTable
      SubnetId:
        Fn::GetAtt:
          - Subnet2
          - SubnetId
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/Subnet2RouteTableAssociation
    Condition: CreateNewVPCCondition
  S3GatewayEndpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      PolicyDocument:
        Statement:
          - Action: s3:PutObject
            Condition:
              StringEquals:
                aws:PrincipalArn:
                  - Fn::Join:
                      - ""
                      - - "arn:"
                        - Ref: AWS::Partition
                        - ":iam::"
                        - Ref: AWS::AccountId
                        - :role/
                        - Fn::FindInMap:
                            - Solution
                            - Data
                            - RoleName
                        - "-"
                        - Ref: AWS::Region
            Effect: Allow
            Principal:
              AWS: "*"
            Resource:
              Fn::Join:
                - ""
                - - "arn:"
                  - Ref: AWS::Partition
                  - ":s3:::"
                  - Ref: CostOptimizerBucket
                  - /*
        Version: "2012-10-17"
      RouteTableIds:
        - Ref: MainRouteTable
      ServiceName:
        Fn::Join:
          - ""
          - - com.amazonaws.
            - Ref: AWS::Region
            - .s3
      VpcId:
        Ref: VPC
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/S3GatewayEndpoint
    Condition: CreateNewVPCCondition
  DynamoDBGatewayEndpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      PolicyDocument:
        Statement:
          - Action: dynamodb:Scan
            Condition:
              StringEquals:
                aws:PrincipalArn:
                  - Fn::Join:
                      - ""
                      - - "arn:"
                        - Ref: AWS::Partition
                        - ":iam::"
                        - Ref: AWS::AccountId
                        - :role/
                        - Fn::FindInMap:
                            - Solution
                            - Data
                            - RoleName
                        - "-"
                        - Ref: AWS::Region
            Effect: Allow
            Principal:
              AWS: "*"
            Resource:
              Fn::Join:
                - ""
                - - "arn:"
                  - Ref: AWS::Partition
                  - ":dynamodb:"
                  - Ref: AWS::Region
                  - ":"
                  - Ref: AWS::AccountId
                  - :table/
                  - Ref: SpokeAccountTable
        Version: "2012-10-17"
      RouteTableIds:
        - Ref: MainRouteTable
      ServiceName:
        Fn::Join:
          - ""
          - - com.amazonaws.
            - Ref: AWS::Region
            - .dynamodb
      VpcId:
        Ref: VPC
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/DynamoDBGatewayEndpoint
    Condition: CreateDynamoDBEndpointCondition
  FlowLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      RetentionInDays: 731
    UpdateReplacePolicy: Retain
    DeletionPolicy: Retain
    Metadata:
      cfn_nag:
        rules_to_suppress:
          - id: W84
            reason: CloudWatch logs are encrypted by the service.
          - id: W86
            reason: CloudWatch logs are set to never expire.
    Condition: CreateNewVPCCondition
  FlowLogRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Action: sts:AssumeRole
            Effect: Allow
            Principal:
              Service: vpc-flow-logs.amazonaws.com
        Version: "2012-10-17"
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/FlowLogRole/Resource
    Condition: CreateNewVPCCondition
  FlowLog:
    Type: AWS::EC2::FlowLog
    Properties:
      DeliverLogsPermissionArn:
        Fn::GetAtt:
          - FlowLogRole
          - Arn
      LogGroupName:
        Ref: FlowLogGroup
      ResourceId:
        Ref: VPC
      ResourceType: VPC
      TrafficType: ALL
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/FlowLog
    Condition: CreateNewVPCCondition
  FlowLogsPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyDocument:
        Statement:
          - Action:
              - logs:CreateLogStream
              - logs:PutLogEvents
              - logs:DescribeLogGroups
              - logs:DescribeLogStreams
            Effect: Allow
            Resource:
              Fn::GetAtt:
                - FlowLogGroup
                - Arn
        Version: "2012-10-17"
      PolicyName: flowlogs-policy
      Roles:
        - Ref: FlowLogRole
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/CostOptimizerVpc/FlowLogsPolicy/Resource
    Condition: CreateNewVPCCondition
  SolutionHelperRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Action: sts:AssumeRole
            Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
        Version: "2012-10-17"
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/UUIDGenerator/UUIDGeneratorFunctionLambdaRole/Resource
  SolutionHelperPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyDocument:
        Statement:
          - Action:
              - logs:CreateLogGroup
              - logs:CreateLogStream
              - logs:PutLogEvents
            Effect: Allow
            Resource:
              Fn::Join:
                - ""
                - - "arn:"
                  - Ref: AWS::Partition
                  - ":logs:"
                  - Ref: AWS::Region
                  - ":"
                  - Ref: AWS::AccountId
                  - :log-group:/
                  - Ref: AWS::Partition
                  - /lambda/*
          - Action: iam:PassRole
            Effect: Allow
            Resource:
              Fn::GetAtt:
                - SolutionHelperRole
                - Arn
          - Action: cloudformation:DescribeStacks
            Effect: Allow
            Resource: "*"
          - Action:
              - xray:PutTraceSegments
              - xray:PutTelemetryRecords
            Effect: Allow
            Resource: "*"
        Version: "2012-10-17"
      PolicyName: SolutionHelperPolicy
      Roles:
        - Ref: SolutionHelperRole
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/UUIDGenerator/UUIDGeneratorFunctionPolicy/Resource
  SolutionHelperFunction:
    Type: AWS::Lambda::Function
    Properties:
      Code:
        S3Bucket:
          Fn::Join:
            - ""
            - - solutions-
              - Ref: AWS::Region
        S3Key: cost-optimizer-for-amazon-workspaces/v2.6.5/uuid_generator.zip
      Description: Solution Helper Lambda Function
      Environment:
        Variables:
          USER_AGENT_STRING: AwsSolution/SO0018/v2.6.5
          LOG_LEVEL:
            Ref: LogLevel
      Handler: uuid_generator/uuid_generator.lambda_handler
      Role:
        Fn::GetAtt:
          - SolutionHelperRole
          - Arn
      Runtime: python3.11
      Tags:
        - Key:
            Fn::FindInMap:
              - Solution
              - Data
              - TagKey
          Value:
            Ref: AWS::StackName
      Timeout: 300
      TracingConfig:
        Mode: Active
    DependsOn:
      - SolutionHelperRole
    Metadata:
      cfn_nag:
        rules_to_suppress:
          - id: W58
            reason: The lambda function has access to write logs
          - id: W89
            reason: The lambda function does not need access to resources in VPC
          - id: W92
            reason: The lambda function only executes on stack creation and deletion and so does not need reserved concurrency.
          - id: W12
            reason: Resource * is necessary for xray:PutTraceSegments and xray:PutTelemetryRecords.
  UUIDGenerator:
    Type: Custom::UUIDGenerator
    Properties:
      ServiceToken:
        Fn::GetAtt:
          - SolutionHelperFunction
          - Arn
      Region:
        Ref: AWS::Region
      DependsOn:
        Fn::GetAtt:
          - SolutionHelperFunction
          - Arn
    UpdateReplacePolicy: Delete
    DeletionPolicy: Delete
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/UUIDGenerator/UUIDCustomResource/Default
  CostOptimizerCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName:
        Fn::FindInMap:
          - Solution
          - Data
          - ClusterName
      ClusterSettings:
        - Name: containerInsights
          Value: enabled
      Tags:
        - Key:
            Fn::FindInMap:
              - Solution
              - Data
              - TagKey
          Value:
            Ref: AWS::StackName
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/EcsClusterResources/EcsCluster
  CostOptimizerAdminRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Action: sts:AssumeRole
            Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
        Version: "2012-10-17"
      RoleName:
        Fn::Join:
          - "-"
          - - Fn::FindInMap:
                - Solution
                - Data
                - RoleName
            - Ref: AWS::Region
    Metadata:
      cfn_nag:
        rules_to_suppress:
          - id: W28
            reason: Static naming is necessary for hub account to assume this role
  CostOptimizerAdminPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyDocument:
        Statement:
          - Action:
              - logs:CreateLogGroup
              - logs:CreateLogStream
              - logs:PutLogEvents
            Effect: Allow
            Resource:
              Fn::Join:
                - ""
                - - "arn:"
                  - Ref: AWS::Partition
                  - ":logs:"
                  - Ref: AWS::Region
                  - ":"
                  - Ref: AWS::AccountId
                  - :log-group:/ecs/wco-task/*
          - Action: ecr:GetAuthorizationToken
            Effect: Allow
            Resource: "*"
          - Action:
              - workspaces:DescribeTags
              - workspaces:DescribeWorkspaces
              - workspaces:DescribeWorkspaceDirectories
              - workspaces:ModifyWorkspaceProperties
              - workspaces:TerminateWorkspaces
              - workspaces:DescribeWorkspacesConnectionStatus
            Effect: Allow
            Resource:
              - Fn::Join:
                  - ""
                  - - "arn:"
                    - Ref: AWS::Partition
                    - ":workspaces:*:"
                    - Ref: AWS::AccountId
                    - :directory/*
              - Fn::Join:
                  - ""
                  - - "arn:"
                    - Ref: AWS::Partition
                    - ":workspaces:*:"
                    - Ref: AWS::AccountId
                    - :workspace/*
              - Fn::Join:
                  - ""
                  - - "arn:"
                    - Ref: AWS::Partition
                    - ":workspaces:*:"
                    - Ref: AWS::AccountId
                    - :workspacebundle/*
          - Action: s3:PutObject
            Effect: Allow
            Resource:
              Fn::Join:
                - ""
                - - "arn:"
                  - Ref: AWS::Partition
                  - ":s3:::"
                  - Ref: CostOptimizerBucket
                  - /*
          - Action: cloudwatch:GetMetricStatistics
            Effect: Allow
            Resource: "*"
          - Action: sts:AssumeRole
            Effect: Allow
            Resource:
              Fn::Join:
                - ""
                - - "arn:"
                  - Ref: AWS::Partition
                  - :iam::*:role/
                  - Fn::FindInMap:
                      - Solution
                      - Data
                      - SpokeAccountWorkspacesRole
                  - "-"
                  - Ref: AWS::Region
        Version: "2012-10-17"
      PolicyName: CostOptimizerAdminPolicy
      Roles:
        - Ref: CostOptimizerAdminRole
    Metadata:
      cfn_nag:
        rules_to_suppress:
          - id: W12
            reason: ecr:GetAuthorizationToken only supports * as the resource
  CostOptimizerDynamoDBPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyDocument:
        Statement:
          - Action: dynamodb:Scan
            Effect: Allow
            Resource:
              Fn::Join:
                - ""
                - - "arn:"
                  - Ref: AWS::Partition
                  - ":dynamodb:"
                  - Ref: AWS::Region
                  - ":"
                  - Ref: AWS::AccountId
                  - :table/
                  - Ref: SpokeAccountTable
        Version: "2012-10-17"
      PolicyName: CostOptimizerDynamoDBPolicy
      Roles:
        - Ref: CostOptimizerAdminRole
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/EcsClusterResources/CostOptimizerDynamoDBPolicy/Resource
    Condition: MultiAccountDeploymentCondition
  CostOptimizerLogs:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName:
        Fn::Join:
          - /
          - - Fn::FindInMap:
                - Solution
                - Data
                - LogGroupName
            - Ref: AWS::StackName
      RetentionInDays: 365
    UpdateReplacePolicy: Retain
    DeletionPolicy: Retain
    Metadata:
      cfn_nag:
        rules_to_suppress:
          - id: W84
            reason: KMS encryption unnecessary for log group
  CostOptimizerTaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      ContainerDefinitions:
        - Cpu: 256
          Environment:
            - Name: LogLevel
              Value:
                Ref: LogLevel
            - Name: DryRun
              Value:
                Ref: DryRun
            - Name: TestEndOfMonth
              Value:
                Ref: TestEndOfMonth
            - Name: SendAnonymousData
              Value:
                Fn::FindInMap:
                  - Solution
                  - Data
                  - SendAnonymousUsageData
            - Name: SolutionVersion
              Value:
                Fn::FindInMap:
                  - Solution
                  - Data
                  - Version
            - Name: SolutionID
              Value:
                Fn::FindInMap:
                  - Solution
                  - Data
                  - ID
            - Name: UUID
              Value:
                Fn::GetAtt:
                  - UUIDGenerator
                  - UUID
            - Name: BucketName
              Value:
                Ref: CostOptimizerBucket
            - Name: ValueLimit
              Value:
                Ref: ValueLimit
            - Name: StandardLimit
              Value:
                Ref: StandardLimit
            - Name: PerformanceLimit
              Value:
                Ref: PerformanceLimit
            - Name: PowerLimit
              Value:
                Ref: PowerLimit
            - Name: PowerProLimit
              Value:
                Ref: PowerProLimit
            - Name: GraphicsLimit
              Value:
                Ref: GraphicsLimit
            - Name: GraphicsProLimit
              Value:
                Ref: GraphicsProLimit
            - Name: MetricsEndpoint
              Value:
                Fn::FindInMap:
                  - Solution
                  - Data
                  - MetricsURL
            - Name: UserAgentString
              Value:
                Fn::Sub:
                  - AwsSolution/${SolutionID}/${Version}
                  - SolutionID:
                      Fn::FindInMap:
                        - Solution
                        - Data
                        - ID
                    Version:
                      Fn::FindInMap:
                        - Solution
                        - Data
                        - Version
            - Name: AutoStopTimeoutHours
              Value:
                Fn::FindInMap:
                  - Solution
                  - Data
                  - AutoStopTimeoutHours
            - Name: Regions
              Value:
                Ref: Regions
            - Name: TerminateUnusedWorkspaces
              Value:
                Ref: TerminateUnusedWorkspaces
            - Name: SpokeAccountDynamoDBTable
              Value:
                Fn::If:
                  - MultiAccountDeploymentCondition
                  - Ref: SpokeAccountTable
                  - Ref: AWS::NoValue
            - Name: NumberOfMonthsForTerminationCheck
              Value:
                Ref: NumberOfMonthsForTerminationCheck
            - Name: InactivityPowerOffDays
              Value:
                Ref: InactivityPowerOffDays
            - Name: InactivityTerminateWarningDays
              Value:
                Ref: InactivityTerminateWarningDays
            - Name: TerminationGracePeriodDays
              Value:
                Ref: TerminationGracePeriodDays
          Essential: true
          Image:
            Fn::FindInMap:
              - Solution
              - Data
              - Image
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group:
                Ref: CostOptimizerLogs
              awslogs-stream-prefix: ecs
              awslogs-region:
                Ref: AWS::Region
          Name: workspace-cost-optimizer
          ReadonlyRootFilesystem: true
      Cpu: "256"
      ExecutionRoleArn:
        Fn::GetAtt:
          - CostOptimizerAdminRole
          - Arn
      Family:
        Fn::FindInMap:
          - Solution
          - Data
          - TaskDefinitionName
      Memory: "1024"
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      TaskRoleArn:
        Fn::GetAtt:
          - CostOptimizerAdminRole
          - Arn
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/EcsClusterResources/EcsTaskDefinition
  InvokeECSTaskRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Action: sts:AssumeRole
            Effect: Allow
            Principal:
              Service: events.amazonaws.com
        Version: "2012-10-17"
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/EcsClusterResources/EventsRuleRole/Resource
  InvokeECSTaskPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyDocument:
        Statement:
          - Action: ecs:RunTask
            Effect: Allow
            Resource:
              - Fn::Join:
                  - ""
                  - - "arn:"
                    - Ref: AWS::Partition
                    - ":ecs:"
                    - Ref: AWS::Region
                    - ":"
                    - Ref: AWS::AccountId
                    - :task-definition/wco-task
              - Fn::Join:
                  - ""
                  - - "arn:"
                    - Ref: AWS::Partition
                    - ":ecs:"
                    - Ref: AWS::Region
                    - ":"
                    - Ref: AWS::AccountId
                    - :task-definition/wco-task:*
          - Action: iam:PassRole
            Effect: Allow
            Resource:
              Fn::GetAtt:
                - CostOptimizerAdminRole
                - Arn
        Version: "2012-10-17"
      PolicyName: InvokeECSTaskPolicy
      Roles:
        - Ref: InvokeECSTaskRole
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/EcsClusterResources/EventsRolePolicy/Resource
  ScheduleRule:
    Type: AWS::Events::Rule
    Properties:
      Description: Rule to trigger WorkSpacesCostOptimizer function on a schedule.
      ScheduleExpression: cron(0 23 * * ? *)
      State: ENABLED
      Targets:
        - Arn:
            Fn::GetAtt:
              - CostOptimizerCluster
              - Arn
          EcsParameters:
            LaunchType: FARGATE
            NetworkConfiguration:
              AwsVpcConfiguration:
                AssignPublicIp: ENABLED
                SecurityGroups:
                  - Fn::If:
                      - CreateNewVPCCondition
                      - Fn::GetAtt:
                          - IntraVPCSecurityGroup
                          - GroupId
                      - Ref: ExistingSecurityGroupId
                Subnets:
                  - Fn::If:
                      - CreateNewVPCCondition
                      - Fn::GetAtt:
                          - Subnet1
                          - SubnetId
                      - Ref: AWS::NoValue
                  - Fn::If:
                      - CreateNewVPCCondition
                      - Fn::GetAtt:
                          - Subnet2
                          - SubnetId
                      - Ref: AWS::NoValue
                  - Fn::If:
                      - UseExistingVPCCondition
                      - Ref: ExistingSubnet1Id
                      - Ref: AWS::NoValue
                  - Fn::If:
                      - UseExistingVPCCondition
                      - Ref: ExistingSubnet2Id
                      - Ref: AWS::NoValue
            PropagateTags: TASK_DEFINITION
            TaskDefinitionArn:
              Fn::GetAtt:
                - CostOptimizerTaskDefinition
                - TaskDefinitionArn
          Id: CostOptimizerTaskDefinition
          RoleArn:
            Fn::GetAtt:
              - InvokeECSTaskRole
              - Arn
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/EcsClusterResources/rule/Resource
  FridayAutoStopRule:
    Type: AWS::Events::Rule
    Properties:
      Description: Rule to trigger WorkSpacesCostOptimizer function for AUTO_STOP on Fridays at 8 PM.
      ScheduleExpression: cron(0 20 ? * FRI *)
      State: ENABLED
      Targets:
        - Arn:
            Fn::GetAtt:
              - CostOptimizerCluster
              - Arn
          EcsParameters:
            LaunchType: FARGATE
            NetworkConfiguration:
              AwsVpcConfiguration:
                AssignPublicIp: ENABLED
                SecurityGroups:
                  - Fn::If:
                      - CreateNewVPCCondition
                      - Fn::GetAtt:
                          - IntraVPCSecurityGroup
                          - GroupId
                      - Ref: ExistingSecurityGroupId
                Subnets:
                  - Fn::If:
                      - CreateNewVPCCondition
                      - Fn::GetAtt:
                          - Subnet1
                          - SubnetId
                      - Ref: AWS::NoValue
                  - Fn::If:
                      - CreateNewVPCCondition
                      - Fn::GetAtt:
                          - Subnet2
                          - SubnetId
                      - Ref: AWS::NoValue
                  - Fn::If:
                      - UseExistingVPCCondition
                      - Ref: ExistingSubnet1Id
                      - Ref: AWS::NoValue
                  - Fn::If:
                      - UseExistingVPCCondition
                      - Ref: ExistingSubnet2Id
                      - Ref: AWS::NoValue
            PropagateTags: TASK_DEFINITION
            TaskDefinitionArn:
              Fn::GetAtt:
                - CostOptimizerTaskDefinition
                - TaskDefinitionArn
          Id: CostOptimizerAutoStopTaskDefinition
          RoleArn:
            Fn::GetAtt:
              - InvokeECSTaskRole
              - Arn
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/EcsClusterResources/FridayAutoStopRule
  RegisterSpokeAccountsFunctionLambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Action: sts:AssumeRole
            Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
        Version: "2012-10-17"
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/RegisterSpokeAccount/RegisterSpokeAccountsFunctionLambdaRole/Resource
    Condition: MultiAccountDeploymentCondition
  RegisterSpokeAccountsFunctionLambdaPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyDocument:
        Statement:
          - Action:
              - logs:CreateLogGroup
              - logs:CreateLogStream
              - logs:PutLogEvents
            Effect: Allow
            Resource:
              Fn::Join:
                - ""
                - - "arn:"
                  - Ref: AWS::Partition
                  - ":logs:"
                  - Ref: AWS::Region
                  - ":"
                  - Ref: AWS::AccountId
                  - :log-group:/
                  - Ref: AWS::Partition
                  - /lambda/*
          - Action:
              - dynamodb:PutItem
              - dynamodb:DeleteItem
            Effect: Allow
            Resource:
              Fn::Join:
                - ""
                - - "arn:"
                  - Ref: AWS::Partition
                  - ":dynamodb:"
                  - Ref: AWS::Region
                  - ":"
                  - Ref: AWS::AccountId
                  - :table/
                  - Ref: SpokeAccountTable
          - Action: iam:PassRole
            Effect: Allow
            Resource:
              Fn::GetAtt:
                - RegisterSpokeAccountsFunctionLambdaRole
                - Arn
          - Action:
              - xray:PutTraceSegments
              - xray:PutTelemetryRecords
            Effect: Allow
            Resource: "*"
        Version: "2012-10-17"
      PolicyName: InvokeECSTaskPolicy
      Roles:
        - Ref: RegisterSpokeAccountsFunctionLambdaRole
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/RegisterSpokeAccount/RegisterSpokeAccountsFunctionLambdaPolicy/Resource
    Condition: MultiAccountDeploymentCondition
  RegisterSpokeAccountsFunction:
    Type: AWS::Lambda::Function
    Properties:
      Code:
        S3Bucket:
          Fn::Join:
            - ""
            - - solutions-
              - Ref: AWS::Region
        S3Key: cost-optimizer-for-amazon-workspaces/v2.6.5/register_spoke_lambda.zip
      Environment:
        Variables:
          USER_AGENT_STRING: AwsSolution/SO0018/v2.6.5
          DDB_TABLE_NAME:
            Ref: SpokeAccountTable
          LOG_LEVEL:
            Ref: LogLevel
      FunctionName:
        Fn::Join:
          - "-"
          - - Fn::FindInMap:
                - Solution
                - Data
                - RegisterLambdaFunctionName
            - Ref: AWS::Region
      Handler: register_spoke_lambda/register_spoke_accounts.lambda_handler
      Role:
        Fn::GetAtt:
          - RegisterSpokeAccountsFunctionLambdaRole
          - Arn
      Runtime: python3.11
      Timeout: 300
      TracingConfig:
        Mode: Active
    DependsOn:
      - RegisterSpokeAccountsFunctionLambdaRole
    Metadata:
      cfn_nag:
        rules_to_suppress:
          - id: W58
            reason: The lambda function has access to write logs
          - id: W89
            reason: The lambda function does not need access to resources in VPC
          - id: W92
            reason: ReservedConcurrentExecutions depends on the number of events for event bus
          - id: W12
            reason: Resource * is necessary for xray:PutTraceSegments and xray:PutTelemetryRecords.
    Condition: MultiAccountDeploymentCondition
  RegisterSpokeAccountsFunctionResourcePolicy:
    Type: AWS::Lambda::Permission
    Properties:
      Action: lambda:InvokeFunction
      FunctionName:
        Fn::GetAtt:
          - RegisterSpokeAccountsFunction
          - Arn
      Principal: "*"
      PrincipalOrgID:
        Ref: OrganizationID
    Metadata:
      cfn_nag:
        rules_to_suppress:
          - id: F13
            reason: Lambda principal is a wildcard to allow persmissions to all accounts in the Organization.
    Condition: MultiAccountDeploymentCondition
  Application:
    Type: AWS::ServiceCatalogAppRegistry::Application
    Properties:
      Description: Service Catalog application to track and manage all your resources for the solution cost-optimizer-for-amazon-workspaces
      Name:
        Fn::Join:
          - "-"
          - - Fn::FindInMap:
                - Solution
                - Data
                - AppRegistryApplicationName
            - Ref: AWS::Region
            - Ref: AWS::AccountId
      Tags:
        ApplicationType: AWS-Solutions
        CloudFoundations:CostOptimizerForWorkspaces:
          Ref: AWS::StackName
        SolutionDomain: CloudFoundations
        SolutionID: SO0018
        SolutionName: cost-optimizer-for-amazon-workspaces
        SolutionVersion: v2.6.5
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/AppRegistryHubResources/AppRegistry/Resource
  AppRegistryApplicationStackAssociation:
    Type: AWS::ServiceCatalogAppRegistry::ResourceAssociation
    Properties:
      Application:
        Fn::GetAtt:
          - Application
          - Id
      Resource:
        Ref: AWS::StackId
      ResourceType: CFN_STACK
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/AppRegistryHubResources/CfnResourceAssociation
  DefaultApplicationAttributeGroup:
    Type: AWS::ServiceCatalogAppRegistry::AttributeGroup
    Properties:
      Attributes:
        applicationType: AWS-Solutions
        version: v2.6.5
        solutionID: SO0018
        solutionName: cost-optimizer-for-amazon-workspaces
      Description: Attribute group for solution information
      Name:
        Fn::Join:
          - "-"
          - - Fn::FindInMap:
                - Solution
                - Data
                - AppRegistryApplicationName
            - Ref: AWS::Region
            - Ref: AWS::AccountId
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/AppRegistryHubResources/DefaultApplicationAttributeGroup/Resource
  AppRegistryApplicationAttributeAssociation:
    Type: AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation
    Properties:
      Application:
        Fn::GetAtt:
          - Application
          - Id
      AttributeGroup:
        Fn::GetAtt:
          - DefaultApplicationAttributeGroup
          - Id
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/AppRegistryHubResources/AttributeGroupAssociation
  ApplicationInsightsConfiguration:
    Type: AWS::ApplicationInsights::Application
    Properties:
      AutoConfigurationEnabled: true
      CWEMonitorEnabled: true
      OpsCenterEnabled: true
      ResourceGroupName:
        Fn::Join:
          - "-"
          - - AWS_AppRegistry_Application
            - Fn::FindInMap:
                - Solution
                - Data
                - AppRegistryApplicationName
            - Ref: AWS::Region
            - Ref: AWS::AccountId
    DependsOn:
      - Application
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/AppRegistryHubResources/ApplicationInsightsConfiguration
  ApplicationShare:
    Type: AWS::RAM::ResourceShare
    Properties:
      AllowExternalPrincipals: false
      Name:
        Ref: AWS::StackName
      PermissionArns:
        - Fn::Join:
            - ""
            - - "arn:"
              - Ref: AWS::Partition
              - :ram::aws:permission/AWSRAMPermissionServiceCatalogAppRegistryApplicationAllowAssociation
      Principals:
        - Fn::Join:
            - ""
            - - "arn:"
              - Ref: AWS::Partition
              - ":organizations::"
              - Ref: ManagementAccountId
              - :organization/
              - Ref: OrganizationID
      ResourceArns:
        - Fn::GetAtt:
            - Application
            - Arn
    Metadata:
      aws:cdk:path: cost-optimizer-for-amazon-workspaces/AppRegistryHubResources/ApplicationShare
    Condition: MultiAccountDeploymentCondition
Outputs:
  BucketName:
    Description: The name of the bucket created by the solution.
    Value:
      Ref: CostOptimizerBucket
  UUID:
    Description: Unique identifier for this solution
    Value:
      Fn::GetAtt:
        - UUIDGenerator
        - UUID
  LogLevel:
    Value:
      Ref: LogLevel
    Export:
      Name: LogLevel
  DryRun:
    Value:
      Ref: DryRun
    Export:
      Name: DryRun
  SendAnonymousData:
    Value:
      Fn::FindInMap:
        - Solution
        - Data
        - SendAnonymousUsageData
    Export:
      Name: SendAnonymousData
  SolutionID:
    Value:
      Fn::FindInMap:
        - Solution
        - Data
        - ID
    Export:
      Name: SolutionID
  SolutionVersion:
    Value:
      Fn::FindInMap:
        - Solution
        - Data
        - Version
    Export:
      Name: SolutionVersion
  TestEndOfMonth:
    Value:
      Ref: TestEndOfMonth
    Export:
      Name: TestEndOfMonth
  ValueLimit:
    Value:
      Ref: ValueLimit
    Export:
      Name: ValueLimit
  StandardLimit:
    Value:
      Ref: StandardLimit
    Export:
      Name: StandardLimit
  PerformanceLimit:
    Value:
      Ref: PerformanceLimit
    Export:
      Name: PerformanceLimit
  PowerLimit:
    Value:
      Ref: PowerLimit
    Export:
      Name: PowerLimit
  PowerProLimit:
    Value:
      Ref: PowerProLimit
    Export:
      Name: PowerProLimit
  GraphicsLimit:
    Value:
      Ref: GraphicsLimit
    Export:
      Name: GraphicsLimit
  GraphicsProLimit:
    Value:
      Ref: GraphicsProLimit
    Export:
      Name: GraphicsProLimit

