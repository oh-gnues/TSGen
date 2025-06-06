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
package com.lts.application;

import com.lts.application.swing.error.ErrorPanel;




public class SimpleExceptionHandler extends ApplicationExceptionHandler
{

	@Override
	public void processException(boolean waitForClose, String message, Throwable throwable)
	{
		try
		{
			ErrorPanel.showException(waitForClose, throwable, message, MODE_OK_DETAILS);
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

	@Override
	public int showAndAsk(String message, Throwable throwable, int mode)
	{
		return ErrorPanel.showAndAsk(message, throwable, mode);
	}

}
