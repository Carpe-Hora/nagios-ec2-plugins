# Copyright 2008-2009 Amazon.com, Inc. or its affiliates.  All Rights
# Reserved.  Licensed under the Amazon Software License (the
# "License").  You may not use this file except in compliance with the
# License. A copy of the License is located at
# http://aws.amazon.com/asl or in the "license" file accompanying this
# file.  This file is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
# the License for the specific language governing permissions and
# limitations under the License.

require 'ec2/platform/linux/tar'
require 'ec2/platform/solaris/constants'
module EC2
  module Platform
    module Solaris
      class Tar < EC2::Platform::Linux::Tar
        class Command < EC2::Platform::Linux::Tar::Command
          EXECUTABLE=EC2::Platform::Solaris::Constants::Utility::TAR
          def initialize(e=EXECUTABLE)
            super e
          end
        end
        class Version < EC2::Platform::Linux::Tar::Version
          def default
            s = `#{Command.new.version.expand}`.strip
            s = nil unless $? == 0
            s
          end
          def self.current
            Version.new
          end
        end
      end
    end
  end
end
