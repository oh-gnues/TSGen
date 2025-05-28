//  Copyright 2006, Clark N. Hobbie
//
//  This file is part of the util library.
//
//  The util library is free software; you can redistribute it and/or modify it
//  under the terms of the Lesser GNU General Public License as published by
//  the Free Software Foundation; either version 2.1 of the License, or (at
//  your option) any later version.
//
//  The util library is distributed in the hope that it will be useful, but
//  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
//  or FITNESS FOR A PARTICULAR PURPOSE.  See the Lesser GNU General Public
//  License for more details.
//
//  You should have received a copy of the Lesser GNU General Public License
//  along with the util library; if not, write to the Free Software Foundation,
//  Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
//
package com.lts.util;


import java.util.Enumeration;
import java.util.Vector;


public class SortTest
{
    public static void main (String[] argv)
    {
        try
        {
            test();
        }
        catch (Throwable t)
        {
            t.printStackTrace();
        }
    }
    
    public static void test ()
    {
        Bag b = new Bag();
        
        for (int i = 0; i < 20; i++)
        {
            Integer theInt = new Integer(i);
            b.addElement(theInt);
        }
        
        Vector v = new Vector();
        Enumeration enu = b.elements();
        while (enu.hasMoreElements())
        {
            v.addElement(enu.nextElement());
        }
        
        System.out.println ("Before sort:");
        enu = v.elements();
        while (enu.hasMoreElements())
        {
            System.out.println (enu.nextElement());
        }
        
        System.out.println();
        System.out.println("After sort:");
        
        VectorSorter.sort(v, new IntegerCompareMethod());
        enu = v.elements();
        while (enu.hasMoreElements())
        {
            System.out.println (enu.nextElement());
        }
        
        System.exit(0);
    }
    
}
