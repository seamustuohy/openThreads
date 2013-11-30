from treelib import Node, Tree


class thread(Tree):
    def __init__(self, uuid):
        self.uuid = uuid
        
    def create_node(self, tag, identifier=None, parent=None, user=None):
        """
        Create a child node for the node indicated by the 'parent' parameter
        @param tag Useless little variable
        @param identifier The message ID of the email
        @param parent The message ID of the parent email
        @param user TODO The user ID of the message sender (the hash given to a user_name email combo)
        """
        node = msg(tag, identifier)
        node.add_user(user)
        self.add_node(node, parent)
        return node
    
    def add_root(self, subject, ID, user_name):
        """Creates a root node if one does not already exist.
        This means you have to be really sure you found the origin node before you go creating a thread-tree or it is going to error out on you.
        TODO: Find out if anyone ever adds references from another tree in their headers. This will impact the absorb thread function which is built for this type of multi-thread scenerio."""
        if getattr(self, "root", False):
            return False
        else:
            self.add_node(subject, ID, None, user_name)
            return True
        
    def add_node(self, subject, ID, parent, user_name):
            #TODO add some samitization and return values for bad data sent to this if root already exists 
        self.create_node(subject, ID, parent, user_name)
        
    def get_root(self):
        """Returns the root node of the current tree structure"""
        return root
    
    def get_node_location(self, ID):
        """Returns a identifier for a nodes location within a tree in relation to the tree itself
        TODO: figure out how to do this to create correlations between messages of similar types
        """
        pass
    
    def list_children(self, ID):
        """ Returns the list of all children of this node """
        pass
    
    def get_decendants(self, ID):
        """Returns the list of all children and all their children of the current node to all leaves."""
        pass
    
    def get_ancestors(self, ID):
        """ Returns the list of all ancestor nodes from current node to the current tree root."""
        pass
    
    def add_child(self, parent, child):
        """ Adds a new child node of the parent node."""
        pass
    
    def get_distance(self, origin, dest):
        """Returns the closest distance between two nodes on the tree """
        pass
    
    def get_common_ancestor(self, origin, dest):
        """Returns the first common ancestor between two nodes."""
        pass
    
    def get_farthest_node(self, ID):
        """Returns the node's farthest decendant node and the distance to it. """
        pass
    
    def get_leaves(self, ID):
        """Returns the list of terminal nodes under this node"""
        pass
    
    def get_midpoint_outgroup(self):
        """Returns the node that divides the current tree into two distance-balanced partitions."""
        pass
    
    def get_partitions(self):
            """It returns the set of all possible partitions under a node."""
            pass
        
    def absorb_thread(self, thread):
        """Check for overlaps between this tree and another thread, and add thread into this tree if compatable. For use when combining multiple parts of broken data sets."""
        pass
        
    def contains(self, ID):
        """Check to see if a node is in this thread.
        @return bool True if node in thread, false if node is not in thread."""
        pass
