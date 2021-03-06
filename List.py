"""
PROJECT 1 - Doubly Linked List + Recursion
Name: Chris Li
"""

from __future__ import annotations  # allow self-reference
from typing import TypeVar, Generic, Callable  # function type
from random import randint, seed
from Project1.Node import DoublyLinkedListNode as Node



T = TypeVar("T")


class List:
    """
    Adaptation of the C++ List implementation where its underlying
    structure is a cyclic Doubly Linked List
    """

    def __init__(self, num: int = None, val: Generic[T] = None, container: list = None) -> None:
        """
        Creates root node and sets its prev and next member variable to itself
        Assigns list with param values given
        :param num: count of val occurrences
        :param val: value to be stored in Node
        :param container: contains elements used in assign
        """
        self.node = Node(None)
        self.node.prev = self.node.next = self.node

        if num or container:
            self.assign(num, val, container)

    def __repr__(self) -> str:
        """
        :return: Represents the list as a string utilizing __str__
        """
        return self.__str__()

    def __eq__(self, other: List) -> bool:
        """
        :param other: compares equality with this List
        :return: True if equal otherwise False
        """

        def is_equal(node1: Node, node2: Node) -> bool:
            if node1 is self.node and node2 is other.node:
                return True
            if node1 is self.node or node2 is other.node or node1 != node2 \
                    or node1.prev != node2.prev:
                return False
            return is_equal(node1.next, node2.next)

        return is_equal(self.node.next, other.node.next)

    def assign(self, num: int = None, val: Generic[T] = None, container: list = None):
        """
        Populates self with nodes using the given parameters
        :param num: represents the number of occurrences of val to assign to list
        :param val: value to have n occurrences
        :param container: used to generate nodes with its contents
        """
        self.clear()
        node = self.node

        if container:
            for item in container:
                node.next = Node(item, prev=node)
                node = node.next
        elif num:
            for _ in range(num):
                node.next = Node(val, prev=node)
                node = node.next

        node.next, self.node.prev = self.node, node

    def clear(self) -> None:
        """
        Resets list by reassigning root nodes' references to itself
        """
        self.node.prev = self.node.next = self.node

    # Implement below - Do not modify function signatures

    def empty(self) -> bool:
        """
        :return: if List contains any additional nodes other than the root node, False else True
        """
        if self.node.next is self.node:
            return True
        return False  # O(1)

    def front(self) -> Node:
        """
        :return: first node in the list or root node if empty
        """
        if self.empty():
            return self.node
        return self.node.next

    def back(self) -> Node:
        """
        :return: last node in the list or root node if empty
        """
        if self.empty():
            return self.node
        return self.node.prev

    def swap(self, other: List) -> None:
        """
        :param other: List to swap contents
        """

        front_self = self.node.prev
        back_self = self.node.next
        front_other = other.node.prev
        back_other = other.node.next

        if self.front() is self.node:
            other.clear()
            other = List(container=[])

        if front_self:
            front_self.next = other.node
        if back_self:
            back_self.prev = other.node
        if front_other:
            front_other.next = self.node
        if back_other:
            back_other.prev = self.node

        self.node.prev = front_other
        self.node.next = back_other
        other.node.prev = front_self
        other.node.next = back_self

    def __str__(self) -> str:
        """
        RECURSIVE
        :return: string representation of linked list
        """
        def to_string(node):
            """string helper"""
            output = node.__str__()
            if node.next is self.node:
                return output
            output += ' <-> '
            output += to_string(node.next)
            return output
        if self.node.next is self.node:
            return ''
        return to_string(self.node.next)

    def size(self) -> int:
        """
        RECURSIVE
        :return: size of list or number of nodes not including the root node
        """
        def size_list(node) -> int:
            if node.next is self.node:
                return 1
            return 1+size_list(node.next)
        if self.front() is self.node:
            return 0
        return size_list(self.node.next)

    def insert(self, position: Node, val: Generic[T], num: int = 1) -> Node:
        """
        RECURSIVE
        Places node before given position with a value of val
        When num is given, insert num occurrences of node
        :param position: Node index to insert new node before
        :param val: value to insert
        :param num: number of insertions of val at position index
        :return: node that points to the first of the newly inserted nodes
        """

        def insert_qaq(node, position, val, num):

            new_node = Node(val)
            new_node.prev = position.prev
            new_node.next = position
            position.prev = new_node
            new_node.prev.next = new_node
            if num != 1:
                insert_qaq(node, position, val, num - 1)

        if num == 0:
            self.assign(container=[None])
            return self
        insert_qaq(self, position, val, num)

    def erase(self, first: Node, last: Node = None) -> Node:
        """
        Erases node or nodes in list from first to, but not including last: [first, last)
        When last is not given, erase only first node
        :param first: position to start erasing (inclusive)
        :param last: position to end erasing (exclusive)
        :return: node that followed the last node erased
        """

        if first is self.node:
            return self.node.next
        elif last is None:
            first.prev.next = first.next
            first.next.prev = first.prev
            print(first.next.prev)
            return first.prev.next
        else:
            first.prev.next = last
            last.prev = first.prev
            return first.prev.next

    def push_front(self, val: Generic[T]) -> None:
        """
        Inserts new Node with value of val in the front of the list
        :param val: value of new Node
        """
        new_node = Node(val)
        self.node.next.prev = new_node
        new_node.next = self.node.next
        new_node.prev = self.node
        self.node.next = new_node

    def push_back(self, val: Generic[T]) -> None:
        """
        Inserts new Node with value of val in the back of the list
        :param val: value of new Node
        """
        new_node = Node(val)
        self.node.prev.next = new_node
        new_node.next = self.node
        new_node.prev = self.node.prev
        self.node.prev = new_node

    def pop_front(self) -> None:
        """
        Erases Node in the front of the list
        """
        temp_node = self.node.next.next
        self.node.next.next.prev = self.node
        self.node.next = temp_node

    def pop_back(self) -> None:
        """
        Erases Node in the back of the list
        """
        temp_node = self.node.prev.prev
        self.node.prev.prev.next = self.node
        self.node.prev = temp_node


    def remove(self, val: Generic[T]) -> None:
        """
        RECURSIVE
        Removes all nodes containing a value of val
        :param val: value to remove
        """

        def remove_node(node: Node) -> Node:
            """remove helper"""
            if node.val == val:
                node.prev.next = node.next
                node.next.prev = node.prev
            node = node.next
            if node is self.node:
                return
            remove_node(node)

        remove_node(self.node)

    def remove_if(self, pred: Callable[[T], bool]) -> None:
        """
        RECURSIVE
        Removes all Nodes with pred returning True
        :param pred: predicate function that returns a boolean
        """
        def remove_node_if(node: Node) -> Node:
            """remove_if helper"""
            if pred(node.val):
                node.next.prev = node.prev
                node.prev.next = node.next
            node = node.next
            if node is self.node:
                return
            remove_node_if(node)
        remove_node_if(self.node.next)

    def reverse(self) -> None:
        """
        RECURSIVE
        Reverses linked list in place
        """
        def reverse_list(node: Node) -> None:
            """reverse helper"""
            temp_node = node.next
            node.next = node.prev
            node.prev = temp_node
            if node.prev is not self.node:
                return reverse_list(node.prev)
        reverse_list(self.node)

    def unique(self) -> None:
        """
        RECURSIVE
        Removes all but one element from every consecutive group of equal elements in the container
        """

        def unique_list(node: Node) -> Node:
            """unique helper"""
            if node.val == node.next.val:
                node.next = node.next.next
                node.next.prev = node

            else:
                node = node.next

            if node.next is self.node:
                return
            unique_list(node)

        unique_list(self.node)

# Application Problem

def fix_playlist(lst: List) -> bool:
    """
    Checks if the given lst is proper, broken, or improper
    It is broken when there is no cycle
    It is improper when lst forms a cycle with a node other than the root node
    Fixes lst if broken in place
    :param lst: List to check and fix cycle
    :return: True if proper or fixed broken cycle else False
    """

    def fix_playlist_helper(slow: Node, fast: Node) -> bool:
        """fix_playlist helper"""
        if slow.next is None:
            slow.next = lst.node
            lst.node.prev = slow
            return True
        elif fast.next is None:
            fast.next = lst.node
            lst.node.prev = fast
            return True
        elif fast.next.next is None:
            fast.next.next = lst.node
            lst.node.prev = fast.next
            return True
        elif slow.next is lst.node or fast.next is lst.node or fast.next.next is lst.node:
            return True
        elif fast.next is slow.next:
            return False
        else:
            return fix_playlist_helper(slow.next, fast.next.next)

    if lst.front() is lst.node:
        return True
    return fix_playlist_helper(lst.node, lst.node.next)
