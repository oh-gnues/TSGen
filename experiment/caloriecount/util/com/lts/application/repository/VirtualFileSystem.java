//  Copyright 2006, Clark N. Hobbie
//
//  This file is part of the com.lts.application library.
//
//  The com.lts.application library is free software; you can redistribute it
//  and/or modify it under the terms of the Lesser GNU General Public License
//  as published by the Free Software Foundation; either version 2.1 of the
//  License, or (at your option) any later version.
//
//  The com.lts.application library is distributed in the hope that it will be
//  useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the Lesser GNU
//  General Public License for more details.
//
//  You should have received a copy of the Lesser GNU General Public License
//  along with the com.lts.application library; if not, write to the Free
//  Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
//  02110-1301 USA
//
package com.lts.application.repository;

import java.io.InputStream;
import java.io.OutputStream;
import java.util.List;

import com.lts.application.ApplicationException;

/**
 * An object that presents a file system interface.
 */
public interface VirtualFileSystem
{
	public InputStream getInputStream(String name) throws ApplicationException;
	public OutputStream getOutputStream (String name, boolean append) throws ApplicationException;
	public boolean removeEntry (String name) throws ApplicationException;
	public List<String> listEntries(String name) throws ApplicationException;
}
